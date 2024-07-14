## basic ring buffer
this is very simple, but working ring buffer.
It was created for working with UART's interrupt in uc.

ring_buffer.c has ring buffer implementation  
ring_buffer.h some simple interface

main.c has example of use.

buffer is char type, size is defined in BUFSIZE in ring_buffer.c

void buffer_put(char c) puts a char into buffer  
char buffer_pop(void) return a char from buffer

for debugging might be useful:
void clear(void)    set all buffer elements to '\0', and reset counters to 0  
void dump(void)     print buffer elements and counters
