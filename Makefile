NAME = Npuzzle

SRC = Main.cpp Npuzzle.cpp

OB = $(SRC:.cpp=.o)

FLAGS = -std=c++11 -O3

CC=g++

all: $(NAME)

$(NAME): $(OB)
		$(CC) -o $(NAME) $(OB)

%.o : %.cpp
		$(CC) $(FLAGS) -c -o  $@ $<

clean:
		rm -f $(OB)

fclean: clean
		rm -f $(NAME)

re: clean all
