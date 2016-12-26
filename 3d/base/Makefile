HEADERS = vertex.h bounding_box.h

OBJECTS = test.o

FLAGS = -std=c++11

default: test.a

%.o: %.cpp $(HEADERS)
	g++ $(FLAGS) -c -g $< -o $@

test.a: $(OBJECTS)
	g++ $(OBJECTS) -o $@

clean:
	rm -f $(OBJECTS)
	rm -f test.a

test:
	./test.a

