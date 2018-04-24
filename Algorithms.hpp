#pragma once

#include <stdlib.h>
#include <map>
#include <algorithm>
// #include <mutex>
// #include <thread>
#include "Npuzzle.hpp"

namespace {
    Coordinates getNumberPozition(Matrix map, int32_t n)
    {
        for (uint32_t x = 0; x < map.size(); x++)
            for (uint32_t y = 0; y < map[x].size(); y++)
                if (map[x][y] == n)
                    return Coordinates(x, y);
        return Coordinates(0, 0);
    }

    __forceinline Coordinates getDestinationPosition(uint32_t mapSize, uint32_t n)
    {
        return Coordinates(n % mapSize ? n / mapSize : n / mapSize - 1, n % mapSize ? n % mapSize - 1 : mapSize);
    }

    uint32_t getR(std::shared_ptr<Npuzzle> n)
    {
        uint32_t r = 0;

        for (uint32_t x = 0; x < n->getMapSize(); x++)
            for (uint32_t y = 0; y < n->getMapSize(); y++)
                if (Coordinates(x, y) == getDestinationPosition(n->getMapSize(), n->getMap()[x][y]))
                    r++;
                else
                    return n->getMapSize() - r / n->getMapSize();
        return n->getMapSize() - r / n->getMapSize();
    }

    uint32_t getM(std::shared_ptr<Npuzzle> n)
    {
        uint32_t m = 0;

        for (uint32_t x = 0; x < n->getMapSize(); x++)
            for (uint32_t y = 0; y < n->getMapSize(); y++)
            {
                Coordinates c = getDestinationPosition(n->getMapSize(), n->getMap()[x][y]);
                m += abs((int32_t)x - (int32_t)c.first) + abs((int32_t)y - (int32_t)c.second);
            }

        return m;
    }

    __forceinline bool isPresentInItems(std::vector<std::shared_ptr<Npuzzle>> all_items, std::shared_ptr<Npuzzle> rhs)
    {
        if (find_if(all_items.begin(), all_items.end(), [rhs] (const std::shared_ptr<Npuzzle>& lhs) { 
            return *lhs == *rhs;
        }) != all_items.end())
            return true;
        return false;
    }

    __forceinline void move(std::vector<std::shared_ptr<Npuzzle>>& items, std::shared_ptr<Npuzzle> n)
    {
        static std::shared_ptr<Npuzzle> m0;
        static std::shared_ptr<Npuzzle> m1;
        static std::shared_ptr<Npuzzle> m2;
        static std::shared_ptr<Npuzzle> m3;

        m0 = std::make_shared<Npuzzle>(*n);
        m1 = std::make_shared<Npuzzle>(*n);
        m2 = std::make_shared<Npuzzle>(*n);
        m3 = std::make_shared<Npuzzle>(*n);

        if (m0->moveRight() != -1)
            items.push_back(m0);
        if (m1->moveLeft() != -1)
            items.push_back(m1);
        if (m2->moveUp() != -1)
            items.push_back(m2);
        if (m3->moveDown() != -1)
            items.push_back(m3);
    }
} //namespace

void printMoves(std::vector<std::shared_ptr<Npuzzle>> v, std::shared_ptr<Npuzzle> n)
{
    for (auto it = v.begin() + 1; it != v.end(); it++)
        std::cout << **it << std::endl;
}

std::vector<std::shared_ptr<Npuzzle>> aRow(std::shared_ptr<Npuzzle> n)
{
    bool solve = false;
    std::vector<std::shared_ptr<Npuzzle>> items;
    items.reserve(30000);
    items.push_back(std::make_shared<Npuzzle>(*n));

    while (!solve)
    {
        partial_sort(items.begin(), items.begin() + 1, items.end(), [](const std::shared_ptr<Npuzzle>& lhs, const std::shared_ptr<Npuzzle>& rhs)
        {
            return (getR(lhs) + getM(lhs) + lhs->getH() + lhs->getG()) < (getR(rhs) + getM(rhs) + rhs->getH() + rhs->getG());
        });

        if (items[0]->getH() == 0)
            solve = true;
        else
        {
            move(items, items[0]);
            items.erase(items.begin());
        }

        std::cout << items.size() << " " << getR(items[0]) << " " << items[0]->getG() << std::endl;
    }

    std::vector<std::shared_ptr<Npuzzle>> result = items[0]->getMoves();
    result.push_back(items[0]);
    return result;
}

std::vector<std::shared_ptr<Npuzzle>> aManhattan(std::shared_ptr<Npuzzle> n)
{
    bool solve = false;
    std::vector<std::shared_ptr<Npuzzle>> items;
    items.reserve(30000);
    items.push_back(std::make_shared<Npuzzle>(*n));

    while (!solve)
    {
        partial_sort(items.begin(), items.begin() + 1, items.end(), [](const std::shared_ptr<Npuzzle>& lhs, const std::shared_ptr<Npuzzle>& rhs)
        {
            return (getM(lhs) + lhs->getG()) < (getM(rhs) + rhs->getG());
        });

        if (items[0]->getH() == 0)
            solve = true;
        else
        {
            move(items, items[0]);
            items.erase(items.begin());
        }

        // std::cout << *items[0] << "\n" << items.size() << " " << items[0]->getG() << " " << items[0]->getH() << std::endl;
    }

    std::vector<std::shared_ptr<Npuzzle>> result = items[0]->getMoves();
    result.push_back(items[0]);
    return result;
}

std::vector<std::shared_ptr<Npuzzle>> aSearch(std::shared_ptr<Npuzzle> n)
{
    bool solve = false;
    std::vector<std::shared_ptr<Npuzzle>> items;
    items.reserve(30000);
    items.push_back(std::make_shared<Npuzzle>(*n));

    while (!solve)
    {
        partial_sort(items.begin(), items.begin() + 1, items.end(), [](const std::shared_ptr<Npuzzle>& lhs, const std::shared_ptr<Npuzzle>& rhs)
        {
            return (lhs->getG() + lhs->getH()) < (rhs->getG() + rhs->getH());
        });

        if ((((items[0])->getH()) == 0))
		{
            solve = true;
		}
        else
        {
            move(items, items[0]);
            items.erase(items.begin());
        }

        std::cout << items.size() << " " << items[0]->getG() << " " << items[0]->getH() << std::endl;
    }

    std::vector<std::shared_ptr<Npuzzle>> result = items[0]->getMoves();
    result.push_back(items[0]);
    return result;
}
