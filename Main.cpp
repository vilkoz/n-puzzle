#include <vector>
#include <memory>
#include <chrono>
#include <string>
#include "Algorithms.hpp"

static void printUsage(uint32_t r)
{
	std::cout << "Usage: ./Npuzzle\n" <<
		"\t[-f pass to file] or [-g size of map (greater than 2)]\n" <<
		"\t[-p true or false (print map)]\n"
		"\t[-a star or manhattan or row]" << std::endl;
	exit(r);
}

enum 	e_arg_type{
	FILE_INPUT,
	IS_GENERATED,
	PRINT_FIELD,
	ALGORITHM_TYPE,
	NUMBER_OF_ARGS
};

const static std::string g_args_flags[] = {
	"-f",
	"-g",
	"-p",
	"-a"
};

std::map<std::string, std::string>			getArgs(int ac, char **av)
{
	std::map<std::string, std::string>		tokens;
	std::string								currentArg;

	for (int i = 0; i < ac; i++)
	{
		currentArg = std::string(av[i]);
		for (int arg_num = 0; arg_num < NUMBER_OF_ARGS; arg_num++)
		{
			if (currentArg == g_args_flags[arg_num] && i != ac - 1)
			{
				tokens[currentArg] = std::string(av[i + 1]);
			}
			else if (i == ac -1)
			{
				throw std::exception();
			}
		}
	}
	return tokens;
}

	/* for (uint32_t i = 1; i < (uint32_t)ac; i += 2) */
	/* { */
	/* 	if (std::string(av[i]) == "-f") */
	/* 	{ */
	/* 		tokens["pass"] = av[i + 1]; */
	/* 		tokens["flagF"] = true; */
	/* 	} */ 
	/* 	else if (std::string(av[i]) == "-g") */
	/* 	{ */
	/* 		tokens["number"] = std::stoi(av[i + 1]); */
	/* 		tokens["flagG"] = true; */
	/* 	} */
	/* 	else if (std::string(av[i]) == "-p") */
	/* 	{ */
	/* 		if (std::string(av[i + 1]) == "true") */
	/* 			tokens["print_field"] = true; */
	/* 		else if (std::string(av[i + 1]) == "false") */
	/* 			tokens["print_field"] = false; */
	/* 		else */
	/* 			throw std::exception(); */
	/* 	} */
	/* 	else if (std::string(av[i]) == "-a") */
	/* 	{ */
	/* 		if (std::string(av[i + 1]) == "star") */
	/* 			tokens["a_search"] = true; */
	/* 		else if (std::string(av[i + 1]) == "manhattan") */
	/* 			tokens["manhattan"] = true; */
	/* 		else if (std::string(av[i + 1]) == "row") */
	/* 			tokens["row"] = true; */
	/* 		else */
	/* 			throw std::exception(); */
	/* 	} */
	/* 	else */
	/* 		throw std::exception(); */
int main(int c, char **v)
{
	std::shared_ptr<Npuzzle>  n;
	std::vector<std::string>  arg;
	std::string               pass;
	uint32_t                  number;
	bool                      flagF = false;
	bool                      flagG = false;
	bool                      a_search = false;
	bool                      manhattan = false;
	bool                      row = false;
	bool                      print_field = false;

	if (c <= 1 || c % 2 != 1)
	{
		printUsage(1);
	}

	try
	{
		getArgs(c, v);
	}
	catch (std::exception &e)
	{
		printUsage(1);
	}

	if ((flagF && flagG) || (number < 3 && flagG)
			|| (!a_search && !manhattan && !row))
	{
		printUsage(1);
	}

	try
	{
		if (flagF)
			n = std::shared_ptr<Npuzzle>(new Npuzzle(pass));
		else
			n = std::shared_ptr<Npuzzle>(new Npuzzle(number));

		if (print_field == true)
			std::cout << *n << std::endl;
	} 
	catch (std::exception &e)
	{
		std::cout <<  e.what() << std::endl;
		return 1;
	}

	if (n->isSolvable() == false)
	{
		std::cout << "Npuzzle is unsolvable" << std::endl;
		return 2;
	}

	std::vector<std::shared_ptr<Npuzzle>> result_moves;
	std::chrono::time_point<std::chrono::system_clock> start, end;


	start = std::chrono::system_clock::now();
	if (row)
		result_moves = aRow(n);
	else if (manhattan)
		result_moves = aManhattan(n);
	else if (a_search)
		result_moves = aSearch(n);
	end = std::chrono::system_clock::now();

	if (print_field == true)
		printMoves(result_moves, n);

	std::cout << "Result: Moves = " << result_moves.size() - 1 << "; Time = " << static_cast<float>(std::chrono::duration_cast<std::chrono::nanoseconds>(end-start).count()) / 1000000000 << "s;" << std::endl;
	return 0;
}
