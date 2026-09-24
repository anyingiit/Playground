// splitter moves top-level declarations of a Go file into sibling files,
// byte-for-byte, and prunes imports that each resulting file no longer uses.
//
// usage: splitter <src.go> <assign.txt>
// assign.txt lines: "<declname> <target-file>"; unlisted decls stay in src.
// A decl's segment is everything after the previous decl's end up to its own end
// (leading blank lines, floating comments, doc comment, decl).
package main

import (
	"bufio"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
	"path"
	"sort"
	"strconv"
	"strings"
)

func declName(d ast.Decl) string {
	switch d := d.(type) {
	case *ast.FuncDecl:
		if d.Recv != nil && len(d.Recv.List) > 0 {
			t := d.Recv.List[0].Type
			if s, ok := t.(*ast.StarExpr); ok {
				t = s.X
			}
			return fmt.Sprintf("%s.%s", t.(*ast.Ident).Name, d.Name.Name)
		}
		return d.Name.Name
	case *ast.GenDecl:
		var names []string
		for _, sp := range d.Specs {
			switch sp := sp.(type) {
			case *ast.TypeSpec:
				names = append(names, sp.Name.Name)
			case *ast.ValueSpec:
				for _, n := range sp.Names {
					names = append(names, n.Name)
				}
			case *ast.ImportSpec:
				return "import"
			}
		}
		return strings.Join(names, ",")
	}
	return "?"
}

func main() {
	src := os.Args[1]
	data, err := os.ReadFile(src)
	must(err)
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, src, data, parser.ParseComments)
	must(err)

	assign := map[string]string{}
	af, err := os.Open(os.Args[2])
	must(err)
	sc := bufio.NewScanner(af)
	for sc.Scan() {
		fs := strings.Fields(sc.Text())
		if len(fs) == 2 {
			assign[fs[0]] = fs[1]
		}
	}

	off := func(p token.Pos) int { return fset.Position(p).Offset }
	var importEnd int
	var header string
	outs := map[string]*strings.Builder{}
	order := []string{}
	get := func(name string) *strings.Builder {
		if b, ok := outs[name]; ok {
			return b
		}
		b := &strings.Builder{}
		outs[name] = b
		order = append(order, name)
		return b
	}
	get(src)
	prev := 0
	used := map[string]bool{}
	for _, d := range f.Decls {
		end := off(d.End())
		if g, ok := d.(*ast.GenDecl); ok && g.Tok == token.IMPORT {
			importEnd = end
			header = string(data[:end])
			prev = end
			continue
		}
		name := declName(d)
		target, ok := assign[name]
		if !ok {
			target = src
		}
		used[name] = true
		get(target).WriteString(string(data[prev:end]))
		prev = end
	}
	get(src).WriteString(string(data[prev:]))
	for k := range assign {
		if !used[k] {
			fmt.Fprintf(os.Stderr, "WARNING: assignment for unknown decl %q\n", k)
		}
	}
	_ = importEnd

	for _, name := range order {
		body := outs[name].String()
		file := pruneImports(header, body)
		must(os.WriteFile(name, []byte(file), 0o644))
		fmt.Println("wrote", name)
	}
}

// pruneImports keeps only import lines whose package name is referenced as
// "<name>." in body.
func pruneImports(header, body string) string {
	fset := token.NewFileSet()
	hf, err := parser.ParseFile(fset, "h.go", header, parser.ImportsOnly)
	must(err)
	bf, err := parser.ParseFile(fset, "b.go", "package x\n"+body, 0)
	must(err)
	refs := map[string]bool{}
	ast.Inspect(bf, func(n ast.Node) bool {
		if se, ok := n.(*ast.SelectorExpr); ok {
			if id, ok := se.X.(*ast.Ident); ok {
				refs[id.Name] = true
			}
		}
		return true
	})
	var drop []int
	for _, is := range hf.Imports {
		p, _ := strconv.Unquote(is.Path.Value)
		name := path.Base(p)
		if is.Name != nil {
			name = is.Name.Name
		}
		if !refs[name] {
			drop = append(drop, fset.Position(is.Pos()).Line)
		}
	}
	sort.Ints(drop)
	lines := strings.Split(header, "\n")
	dropSet := map[int]bool{}
	for _, l := range drop {
		dropSet[l] = true
	}
	var out []string
	for i, l := range lines {
		if dropSet[i+1] {
			continue
		}
		out = append(out, l)
	}
	return strings.Join(out, "\n") + body
}

func must(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
