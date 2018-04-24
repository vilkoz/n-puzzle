#include "Argparser.hpp"

ArgparserValues::ArgparserValues(void):
	inputType(GENERATED_INPUT),
	algorithmType(ALGO_NOT_SET),
	size(3),
	printEnabled(true),
	fileName("")
{
}

Argparser::Argparser(int &ac, char **&av, std::vector<std::string> &flags,
				std::vector<eArgValueType> &flagTypes, std::vector<eConfigValue> &configValues):
	_flags(flags),
	_flagTypes(flagTypes),
	_configValues(configValues)
{
	std::string								currentArg;

	for (int i = 0; i < ac; i++)
	{
		currentArg = std::string(av[i]);
		for (int arg_num = 0; arg_num < _flags.size(); arg_num++)
		{
			if (currentArg == _flags[arg_num] && i != ac - 1)
			{
				_parseFlagValue(currentArg, std::string(av[i + 1]), _configValues[arg_num]);
			}
			else if (currentArg == _flags[arg_num] && i == ac -1)
			{
				throw std::invalid_argument(currentArg);
			}
		}
	}
}

void		Argparser::_parseFlagValue(std::string &flag, std::string value, eConfigValue configValue)
{
	switch (configValue) {
		case CONFIG_INPUT_TYPE:
			if (flag == "-f")
			{
				_values.inputType = FILE_INPUT;
				_values.fileName = value;
			}
			else
			{
				_values.inputType = GENERATED_INPUT;
				_values.size = stol(value);
			}
			break;
		case CONFIG_ALGORITHM_TYPE:
			if (value[0] == 'm')
			{
				_values.algorithmType = ALGO_MANHATTAN;
			}
			else if (value[0] == 's')
			{
				_values.algorithmType = ALGO_A_SEARCH;
			}
			else if (value[0] == 'r')
			{
				_values.algorithmType = ALGO_ROW;
			}
			else
			{
				throw std::invalid_argument("not found algo type - " + value);
			}
		case CONFIG_IS_PRINT_ENABLED:
			_values.printEnabled = (value == "true");
			break;
	}
}

ArgparserValues		&Argparser::getValues(void)
{
	return _values;
}
