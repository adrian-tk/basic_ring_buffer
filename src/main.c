#include <stdio.h>
//#define BUFSIZE 8
#include "ring_buffer.h"

//char buffer[BUFSIZE];

char short_message;
char message[] = "hello";
int num = 0;
void talking(void);
void hearing(void);


void talking(void){
	if (num > 4){
		num=0;
	}
	short_message = message[num];
	printf("foo speak: %c\n\r", short_message);
	num++;
	buffer_put(short_message);
}

void hearing(void){
	char element;
	element = buffer_pop();
	printf("bar hear: %c\n\r", element);
}
	
int main(void){

	printf("=====case 1======\n\r");
	num = 0;
	clear();
	talking();
	hearing();
	printf("=====case 2======\n\r");
	clear();
	num = 0;
	talking();
	hearing();
	talking();
	hearing();
	talking();
	hearing();
	talking();
	hearing();
	printf("=====case 3======\n\r");
	num = 0;
	clear();
	talking();
	talking();
	talking();
	hearing();
	talking();
	talking();
	talking();
	hearing();
	printf("=====case 4======\n\r");
	num = 0;
	clear();
	talking();
	hearing();
	hearing();
	hearing();
	talking();
	hearing();
	hearing();
	hearing();
}
