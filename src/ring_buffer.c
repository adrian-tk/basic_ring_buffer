#include <stdio.h>
#define BUFSIZE 32

char buffer[BUFSIZE];
int put_position = 0;
int pop_position = 0;

int buffer_put(char c){
	//check if not full
	int tmp = put_position + 1;
	if (tmp > BUFSIZE-1){
		tmp = 0;
	}
	if (!(pop_position == tmp)){
		buffer[put_position]=c;
		put_position++;
		if (put_position == BUFSIZE){
			put_position = 0;
		}
		return 0;
	}
	else{
		printf("WARNING: buffer is full, reject new data\n\r");
		return 1;
	}

}

char buffer_pop(void){
	char c = '\0';
	//check if not empty
	if (pop_position != put_position){
		c = buffer[pop_position];
		pop_position++;
		if (pop_position == BUFSIZE){
			pop_position = 0;
		}
	}
	else{
		printf("INFO: buffer is empty, can't read\n\r");
	}
	return c;
}
void dump(void){
	printf("DEBUG: buffer: %s\n\r", buffer);
	printf("DEBUG: put_position: %d\n\r", put_position);
	printf("DEBUG: pop_position: %d\n\r", pop_position);
}

void clear(void){
	pop_position = 0;
	put_position = 0;
	for(int i=0; i<BUFSIZE; i++){
		buffer[i]='\0';
	}
}
