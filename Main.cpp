#include <vector>
#include <memory>
#include <chrono>
#include <string>
#include "Algorithms.hpp"
#include "Argparser.hpp"

static void printUsage(uint32_t r)
{
	std::cout << "Usage: ./Npuzzle\n" <<
		"\t[-f pass to file] or [-g size of map (greater than 2)]\n" <<
		"\t[-p true or false (print map)]\n"
		"\t[-a star or manhattan or row]" << std::endl;
	exit(r);
}

int main(int c, char **v)
{
	std::shared_ptr<Npuzzle>		n;
	ArgparserValues					config;

	if (c <= 1 || c % 2 != 1)
	{
		printUsage(1);
	}

	try
	{
		std::vector<std::string>	flags = {
			"-f",
			"-g",
			"-a",
			"-p"
		};
		std::vector<eArgValueType>	argTypes = {
			STRING,
			INT,
			STRING,
			BOOL,
		};
		std::vector<eConfigValue>	argConfigValues = {
			CONFIG_INPUT_TYPE,
			CONFIG_INPUT_TYPE,
			CONFIG_ALGORITHM_TYPE,
			CONFIG_IS_PRINT_ENABLED
		};
		Argparser					argParser(c, v, flags, argTypes, argConfigValues);
		config = argParser.getValues();
	}
	catch (std::exception &e)
	{
		std::cout << e.what() << std::endl;
		printUsage(1);
	}

	if ((config.size < 3 && config.inputType == GENERATED_INPUT)
			|| (config.algorithmType == ALGO_NOT_SET))
	{
		printUsage(1);
	}

	try
	{
		if (config.inputType == FILE_INPUT)
			n = std::shared_ptr<Npuzzle>(new Npuzzle(config.fileName));
		else
			n = std::shared_ptr<Npuzzle>(new Npuzzle(config.size));
		if (config.printEnabled)
			std::cout << *n << std::endl;
	} 
	catch (std::exception &e)
	{
		std::cout <<  e.what() << std::endl;
		return 1;
	}

	/* if (n->isSolvable() == false) */
	/* { */
	/* 	std::cout << "Npuzzle is unsolvable" << std::endl; */
	/* 	return 2; */
	/* } */

	std::vector<std::shared_ptr<Npuzzle>> result_moves;
	std::chrono::time_point<std::chrono::system_clock> start, end;


	start = std::chrono::system_clock::now();
	if (config.algorithmType == ALGO_ROW)
		result_moves = aRow(n);
	else if (config.algorithmType == ALGO_MANHATTAN)
		result_moves = aManhattan(n);
	else if (config.algorithmType == ALGO_A_SEARCH)
		result_moves = aSearch(n);
	end = std::chrono::system_clock::now();

	if (config.printEnabled)
		printMoves(result_moves, n);

	std::cout << "Result: Moves = " << result_moves.size() - 1 << "; Time = " << static_cast<float>(std::chrono::duration_cast<std::chrono::nanoseconds>(end-start).count()) / 1000000000 << "s;" << std::endl;
	return 0;
}
