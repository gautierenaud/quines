import codecs

code = b"7072696e742827696d706f727420636f6465637327290a7072696e742827636f6465203d272c20636f6465290a0a7072696e7428636f646563732e6465636f646528636f64652c202768657827292e6465636f6465282775746638272929"

print('import codecs')
print('code =', code)
print(codecs.decode(code, 'hex').decode('utf8'))

# uncomment this code to show how to create the 'code' string
# code = b"print('import codecs')\nprint('code =', code)\n\nprint(codecs.decode(code, 'hex').decode('utf8'))"
# print(codecs.encode(code, "hex"))
