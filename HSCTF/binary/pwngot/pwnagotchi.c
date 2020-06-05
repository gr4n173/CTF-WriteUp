#include <stdio.h>                   
#include <stdlib.h>                  
#include <string.h>                  
#include <stdbool.h>                 
#include <unistd.h>                  
#include <time.h>                    

bool hungry = true;                  
bool sleepy = true;                  
bool once = false;                   

void eat() {                         
  puts("om nom nom");                
  hungry = false;                    
}                                    

void zzz() {                         
  puts("zzz...");                    
  sleep((rand() % 3) + 1);                                                 
  sleepy = false;                    
}                                    

int main() {                         
    gid_t gid = getegid();                                                 
    setresgid(gid, gid, gid);                                              

    setvbuf(stdin, NULL, _IONBF, 0);                                       
    setvbuf(stdout, NULL, _IONBF, 0);                                      

  srand(time(0));
  if (once && (sleepy || hungry)) {
    puts("\n\\ (•-•) /\n");
    puts("This is weird...\n");
    return 0;
  }

  once = true;

  char buffer[8];
  puts("Enter your pwnagotchi's name: ");
  gets(buffer);

  if (!hungry && !sleepy) {
    puts("\n\\ (•◡•) /\n");
    printf("%s is happy!\n", buffer);
  }
  else {
    puts("\n\\ (•-•) /\n");
    printf("%s is not happy!\n", buffer);
  }

  return 0;
}

