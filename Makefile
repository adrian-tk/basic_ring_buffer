# makefile for pc 
#
# 2024-07-13
# Adrian Tomczyk
# adrian.tk@gmail.com
#
# 2024-07-05 initial version
# 2024-07-13 create directories for project

# directories
SRC_DIR := src
OBJ_DIR := build
# or . intead of bin if want to build in current dir
BIN_DIR := bin

# phony don't create file
.PHONY: clean all compile-all

#name of output file
PROG := $(BIN_DIR)/main.elf

#CC = avr-gcc
CC = gcc

#OC = avr-objcopy
OC = gcc-objcopy

CFLAGS = -Wall \
	     -c \
	     -std=gnu99

# C PreProcessor flags
# 
CPPFLAGS := -Iinclude -MMD -MP

LDFLAGS = -Llib

LDLIBS =

OCFLAGS = 

#SRCS = main.c ring_buffer.c
SRCS := $(wildcard $(SRC_DIR)/*.c)

#OBJS := $(SRCS:.c=.o)
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# targets

# default target
#all: $(OBJS)
#	$(CC) $(OBJS) $(LDFLAGS) -o $(PROG)
all: $(PROG)

# LDFLAGS shall be before objects, LDLIBS after.
$(PROG): $(OBJS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

#compile-all: $(SRCS)
#	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS)
#
#%.i: %.c
#	$(CC) $(CFLAGS) $(INCLUDES) -E $< -o $@
#
#%.asm: %.c
#	$(CC) $(CFLAGS) $(INCLUDES) -S $< -o $@

#clean: 
#	rm -f $(PROG)	\
#		$(PROG:.elf=.hex)	\
#		$(PROG:.elf=.map)	\
#	   	$(SRCS:.c=.o) \
#	   	$(SRCS:.c=.d) \
#	   	$(SRCS:.c=.asm) \
#	   	$(SRCS:.c=.i) 

#clean:
#	@$(RM) -rv $(BIN_DIR) $(OBJ_DIR)
clean:
	@$(RM) -rv $(BIN_DIR)/* $(OBJ_DIR)/*

# GCC, Cland, or other dependency generator
# might create .d file with Makefile rules,
# include it here
-include $(OBJS:.o=.d)

