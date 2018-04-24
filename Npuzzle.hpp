#pragma once

#include <vector>
#include <iostream>
#include <memory>
#include <algorithm>

#define __forceinline __attribute__((always_inline))

typedef std::pair<uint32_t, uint32_t>       Coordinates;
typedef std::vector<std::vector<int32_t>>   Matrix;

class Npuzzle {
public:
    Npuzzle(std::string pass);
    Npuzzle(uint32_t size);

    __forceinline uint32_t getG() const
    {
        return _moves.size();
    }

    __forceinline std::vector<std::shared_ptr<Npuzzle>>  getMoves() const
    {
        return _moves;
    }

    __forceinline Matrix getMap() const
    {
        return _map;
    }
    
    __forceinline uint32_t getMapSize() const
    {
        return _mapSize;
    }

    __forceinline int32_t getRight(Coordinates index) const
    {
        return index.second <= _mapSize - 2 ? _map[index.first][index.second + 1] : -1;
    }

    __forceinline int32_t getLeft(Coordinates index) const
    {
        return index.second >= 1 ? _map[index.first][index.second - 1] : -1;
    }

    __forceinline int32_t getDown(Coordinates index) const
    {
        return index.first <= _mapSize - 2 ? _map[index.first + 1][index.second] : -1;
    }

    __forceinline int32_t getUp(Coordinates index) const
    {
        return index.first >= 1 ? _map[index.first - 1][index.second] : -1;
    }

    __forceinline Coordinates getEmptyIndex() const
    {
        return _emptyIndex;
    }

    friend std::ostream &operator <<(std::ostream& stream, const Npuzzle& obj);

    friend bool operator==(const Npuzzle& lhs, const Npuzzle& rhs);

    uint32_t                getH();
    int32_t                 moveLeft();
    int32_t                 moveRight();
    int32_t                 moveUp();
    int32_t                 moveDown();
    bool                    isSolvable();

private:
    int32_t                                 _fileValidation(const std::vector<std::string>);
    void                                    _generateMap();
    void                                    _findEptyIndex();
    std::vector<std::shared_ptr<Npuzzle>>   _moves;
    uint32_t                                _mapSize;
    Matrix                                  _map;
    Coordinates                             _emptyIndex;
};
