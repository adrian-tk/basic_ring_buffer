#ifndef RING_BUFFER_H
#define RING_BUFFER_H

/* This function put a char to a ring buffer
 * Input:
 * 	char: ASCII character to put into a buffer
 * Output:
 * 	0 - succes
 * 	1 - no place in buffer. Buffer will no overwrite,
 * 		additional values will be discarded.
 */
void buffer_put(char c);

/* This function get a char from a buffer.
 * Input:
 * 	void
 * Output:
 * 	char from a buffer, or '\0' when buffer is empty
 * 	when buffer is empty fucntion printf INFO about it.
 */
char buffer_pop(void);


//for debugging
void dump(void);
void clear(void);

#endif
