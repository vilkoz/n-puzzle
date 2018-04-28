#include "Npuzzle.hpp"

#include <sstream>
#include <fstream>
#include <iomanip>
#include <cmath>

namespace {
	uint32_t readFromFile(std::vector<std::string> &file, const std::string pass)
	{
		std::ifstream f;
		std::string line;

		f.open(pass.c_str());
		if (!f.good())
			return -1;

		while (getline(f, line))
			file.push_back(line);

		return 0;
	}

	std::vector<std::string> split(const std::string str, const char delim)
	{
		std::stringstream ss;
		std::string item;
		std::vector<std::string> res;

		ss.str(str);
		while (getline(ss, item, delim))
			if (item.size())
				res.push_back(item);

		return res;
	}

	__forceinline bool isPresentInItems(std::vector<std::shared_ptr<Npuzzle>> all_items, Npuzzle rhs)
	{
		if (find_if(all_items.begin(), all_items.end(), [rhs] (const std::shared_ptr<Npuzzle>& lhs) {return *lhs == rhs;}) != all_items.end())
			return true;
		return false;
	}
} // namespace

Npuzzle::Npuzzle(std::string pass)
{
	std::vector<std::string> file;

	if (readFromFile(file, pass) == -1)
		throw std::invalid_argument("Error: Npuzzle stopped, invalid pass to file");
	
	if (_fileValidation(file) == -1)
		throw std::invalid_argument("Error: Invalid syntax in file");
}

Npuzzle::Npuzzle(uint32_t size) : _mapSize(size)
{
	_generateMap();
	for (auto row: _map)
	{
		for (auto item: row)
		{
			std::cerr << item << " ";
		}
		std::cerr << std::endl;
	}
}

__forceinline int32_t Npuzzle::moveUp()
{
	std::shared_ptr<Npuzzle> c = std::make_shared<Npuzzle>(*this);
	int32_t tmp;

	if (_emptyIndex.first <= _mapSize - 2)
	{
		tmp = _map[_emptyIndex.first][_emptyIndex.second];
		_map[_emptyIndex.first][_emptyIndex.second] =  _map[_emptyIndex.first + 1][_emptyIndex.second];
		_map[_emptyIndex.first + 1][_emptyIndex.second] = tmp;
		_emptyIndex.first++;
	}
	else
		return -1;

	if (!isPresentInItems(_moves, *this))
		_moves.push_back(c);
	else
		return -1;

	return 0;
}

__forceinline int32_t Npuzzle::moveDown()
{
	std::shared_ptr<Npuzzle> c = std::make_shared<Npuzzle>(*this);
	int32_t tmp;

	if (_emptyIndex.first >= 1)
	{
		tmp = _map[_emptyIndex.first][_emptyIndex.second];
		_map[_emptyIndex.first][_emptyIndex.second] =  _map[_emptyIndex.first - 1][_emptyIndex.second];
		_map[_emptyIndex.first - 1][_emptyIndex.second] = tmp;
		_emptyIndex.first--;
	}
	else
		return -1;

	if (!isPresentInItems(_moves, *this))
		_moves.push_back(c);
	else
		return -1;

	return 0;
}

__forceinline int32_t Npuzzle::moveRight()
{
	std::shared_ptr<Npuzzle> c = std::make_shared<Npuzzle>(*this);
	int32_t tmp;

	if (_emptyIndex.second >= 1)
	{
		tmp = _map[_emptyIndex.first][_emptyIndex.second];
		_map[_emptyIndex.first][_emptyIndex.second] =  _map[_emptyIndex.first][_emptyIndex.second - 1];
		_map[_emptyIndex.first][_emptyIndex.second - 1] = tmp;
		_emptyIndex.second--;
	}
	else
		return -1;

	if (!isPresentInItems(_moves, *this))
		_moves.push_back(c);
	else
		return -1;

	return 0;
}

__forceinline int32_t Npuzzle::moveLeft()
{
	std::shared_ptr<Npuzzle> c = std::make_shared<Npuzzle>(*this);
	int32_t tmp;

	if (_emptyIndex.second <= _mapSize - 2)
	{
		tmp = _map[_emptyIndex.first][_emptyIndex.second];
		_map[_emptyIndex.first][_emptyIndex.second] =  _map[_emptyIndex.first][_emptyIndex.second + 1];
		_map[_emptyIndex.first][_emptyIndex.second + 1] = tmp;
		_emptyIndex.second++;
	}
	else
		return -1;

	if (!isPresentInItems(_moves, *this))
		_moves.push_back(c);
	else
		return -1;

	return 0;
}

void Npuzzle::_generateMap()
{
	std::vector<int32_t> tmp;

	srand(time(0));
	while (tmp.size() != (_mapSize * _mapSize)) {
		int32_t    var;
		bool	   found = false;

		var = rand() % (_mapSize * _mapSize);
		for (uint32_t i = 0; i < tmp.size() && !found; i++)
			if (tmp[i] == var)
				found = true;
		if (!found)
			tmp.push_back(var);
	}

	for (uint32_t i = 0; i < tmp.size(); i++){
		std::vector<int32_t> tmpLine;

		while (tmpLine.size() != _mapSize && i < tmp.size())
			tmpLine.push_back(tmp[i++]);
		i--;
		_map.push_back(tmpLine);
	}

	_findEptyIndex();
}

int32_t Npuzzle::_fileValidation(std::vector<std::string> file) {
	for (uint32_t i = 0; i < file.size(); i++)
		for (uint32_t x = 0; x < file[i].size(); x++)
			if (file[i][x] == '#')
				file[i].erase (file[i].begin() + x, file[i].end());

	for (uint32_t i = 1; i - 1 < file.size(); i++)
		if (!file[i - 1].size())
		{
			file.erase(file.begin() + i - 1);
			i = 0;
		}

	if (file.size() < 4)
		return -1;

	for (uint32_t i = 0; i < file[0].size(); i++)
		if (!(file[0][i] >= '0' && file[0][i] <= '9'))
			return -1;

	_mapSize = stoi(file[0]);
	if (file.size() != 1 + _mapSize)
		return -1;

	for (uint32_t i = 1; i < file.size(); i++)
	{
		std::vector<std::string>	tmp;
		std::vector<int32_t>		tmpMapLine;

		tmp = split(file[i], ' ');
		if (tmp.size() != _mapSize)
			return -1;
		for (uint32_t k = 0; k < tmp.size(); k++)
		{
			for (uint32_t p = 0; p < tmp[k].size(); p++)
				if (!(tmp[k][p] >= '0' && tmp[k][p] <= '9'))
					return -1;

			tmpMapLine.push_back(stoi(tmp[k]));
		}

		_map.push_back(tmpMapLine);
	}

	if (_map.size() != _mapSize)
		return -1;

	for (int i = 0; i < _mapSize * _mapSize; i++)
	{
		bool found = false;

		for (uint32_t x = 0; x < _map.size() && !found; x++)
			for (uint32_t y = 0; y < _map[x].size() && !found; y++)
				if (_map[x][y] == i)
					found = true;

		if (!found)
			return -1;
	}

	_findEptyIndex();

	return 0;
}

__forceinline uint32_t Npuzzle::getH()
{
	int32_t dst = 1;
	uint32_t h = _mapSize * _mapSize - 1;
 
	std::for_each(_map.begin(), _map.end(), [&dst, &h](std::vector<int32_t> &it){
		std::for_each(it.begin(), it.end(), [&dst, &h](int32_t &n){
			if (dst == n)
				h--;
			dst++;
		});
	});

	return h;
}

void Npuzzle::_findEptyIndex()
{
	for (uint32_t x = 0; x < _map.size(); x++)
		for (uint32_t y = 0; y < _map[x].size(); y++)
			if (_map[x][y] == 0)
			{
				_emptyIndex.first = x;
				_emptyIndex.second = y;
				break;
			}
}

std::ostream &operator <<(std::ostream& stream, const Npuzzle &obj)
{
	uint32_t	t = 1;

	while (pow(10, t) < obj.getMapSize() * obj.getMapSize())
		t++;

	for (uint32_t x = 0; x < obj.getMapSize(); x++)
	{
		for (uint32_t y = 0; y < obj.getMapSize(); y++)
		{
			stream << std::setw(t + 2);
			stream << obj.getMap()[x][y];
		}
		stream << '\n';
	}

	return stream;
}

__forceinline bool operator==(const Npuzzle& lhs, const Npuzzle& rhs)
{
	if (lhs.getEmptyIndex() == rhs.getEmptyIndex())
	{
		Matrix m1 = lhs.getMap();
		Matrix m2 = rhs.getMap();

		for (auto it1 = m1.begin(), it2 = m2.begin(); it1 != m1.end(); it1++, it2++)
			if (std::equal(it1->begin(), it1->end(), it2->begin()) == false)
				return false;

		return true;
	}

	return false;
}

bool Npuzzle::isSolvable()
{
	int32_t inv = 0;

	for (uint32_t x = 0; x < _map.size(); x++)
	{
		for (uint32_t y = 0; y < _map[x].size(); y++)
		{
			int32_t src = _map[x][y];

			for (uint32_t xi = x; xi < _map.size(); xi++)
			{
				for (uint32_t yi = y; yi < _map[xi].size(); yi++)
				{
					if (src > _map[xi][yi] && src != 0 && _map[xi][yi] != 0)
					{
						inv++;
					}
				}
			}
		}
	}

	if (_mapSize % 2 != 0)
	{
		if (inv % 2 == 0)
			return false;
		else
			return true;
	}
	else
		std::cerr << "Map size should not be even!" << std::endl;
	return false;
}
