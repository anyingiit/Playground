Fixes #273

`StringByte` passes the result of `base64_decode($value, true)` straight into `base64_encode()`. In strict mode, `base64_decode()` returns `false` for input that isn't valid base64, such as `%%%`. On PHP 8, `base64_encode(false)` then throws a `TypeError`, so a request or response with a bad `format: byte` value crashes the validator instead of failing the format check.

This change returns `false` when decoding fails, following the same pattern as `StringDate`. Valid values still go through the existing round-trip comparison, so their behaviour is unchanged.

I added `tests/Schema/TypeFormats/StringByteTest.php` in the same style as the other format tests, with green and red data providers. Without the fix, two of the red cases (`%%%` and a misplaced `=`) fail with the `TypeError`.

How I checked it:
- `vendor/bin/phpunit` passes: 438 tests, 519 assertions.
- `vendor/bin/phpcs` is clean on the two changed files.
- PHPStan reports no errors on them at level 6. I used PHPStan 2.x without the phpstan extensions, because the phpstan 1.x packages wouldn't install in my environment.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as described above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it. No hard feelings at all 🙂
