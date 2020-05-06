# Custom password dictionary generator
Simple script to create a wordlist for a specific target.

## Usage
```bash
:~# python3 ./custom_password_dictionary_generator.py word [word [word..n]] > wordlist.lst
```

### Example
```bash
:~# python3 ./custom_password_dictionary_generator.py h[i1] y[oO0]u > wordlist.lst
:~# cat wordlist.lst

hi
h1
hiyou
hiyOu
hiy0u
h1you
h1yOu
h1y0u
you
yOu
y0u
youhi
youh1
yOuhi
yOuh1
y0uhi
y0uh1
```
