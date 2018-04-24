#pragma once
#include <vector>
#include <iostream>
#include <exception>

enum		eArgValueType
{
	STRING,
	INT,
	BOOL
};

enum	eInputType
{
	FILE_INPUT,
	GENERATED_INPUT
};

enum	eAlgorithmType
{
	ALGO_A_SEARCH,
	ALGO_ROW,
	ALGO_MANHATTAN,
	ALGO_NOT_SET
};

enum	eConfigValue
{
	CONFIG_INPUT_TYPE,
	CONFIG_ALGORITHM_TYPE,
	CONFIG_IS_PRINT_ENABLED
};

class	ArgparserValues
{
	public:
		ArgparserValues(void);
		eInputType		inputType;
		eAlgorithmType	algorithmType;
		int				size;
		bool			printEnabled;
		std::string		fileName;
};

class	Argparser
{
	public:
		Argparser(int &ac, char **&av, std::vector<std::string> &flags,
				std::vector<eArgValueType> &flagTypes, std::vector<eConfigValue> &configValues);
		ArgparserValues			&getValues(void);
	private:
		void								_parseFlagValue(std::string &flag, std::string s, eConfigValue configValue);
		std::vector<std::string>			_flags;
		std::vector<eArgValueType>			_flagTypes;
		std::vector<eConfigValue>			_configValues;
		ArgparserValues						_values;
};
