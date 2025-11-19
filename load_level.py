

import json
import os
from typing import Any, Dict, List, Optional, Callable

from board import Board
from coordinate import Coordinate
from number_block import NumberBlock
from operator_block import OperatorBlock
from goal_block import GoalBlock
from hole import Hole
from player import Player
from wall import Wall


def read_json_file(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_level_json(level_json: Dict[str, Any]):
    rows = int(level_json.get("rows", 0))
    cols = int(level_json.get("cols", 0))
    raw_cells = level_json.get("cells", [])
    parsed_cells = []
    for c in raw_cells:
        cell = dict(c)
        cell["row"] = int(cell["row"])
        cell["col"] = int(cell["col"])
        parsed_cells.append(cell)
    return rows, cols, parsed_cells


def build_board_from_json(
    level_json: Dict[str, Any],
    board: Optional[Board] = None,
    mapping: Optional[Dict[str, Callable[[Board, Dict[str, Any]], None]]] = None,
) -> Board:
    rows, cols, cells = parse_level_json(level_json)

    if board is None:
        board = Board(width=cols, height=rows)

    if mapping is None:
        def _add_agent(b: Board, cell: Dict[str, Any]):
            b.add_player(Player(cell["col"], cell["row"]))

        def _add_target_as_hole(b: Board, cell: Dict[str, Any]):
            b.add_hole(Hole(cell["col"], cell["row"]))

        def _add_number(b: Board, cell: Dict[str, Any]):
            n = int(cell.get("number", 0))
            b.add_number_block(NumberBlock(cell["col"], cell["row"], n))

        def _add_operation(b: Board, cell: Dict[str, Any]):
            op = cell.get("operation", "+")
            b.add_operator_block(OperatorBlock(cell["col"], cell["row"], op))

        def _add_door_as_goal(b: Board, cell: Dict[str, Any]):
            value = int(cell.get("value", 0))
            b.add_goal_block(GoalBlock(cell["col"], cell["row"], value))

        def _add_block_as_wall(b: Board, cell: Dict[str, Any]):
            b.add_wall(Wall(cell["col"], cell["row"]))

        mapping = {
            "agent": _add_agent,
            "target": _add_target_as_hole,
            "number": _add_number,
            "operation": _add_operation,
            "door": _add_door_as_goal,
            "block": _add_block_as_wall,
        }

    for cell in cells:
        t = cell.get("type")
        handler = mapping.get(t)
        if handler:
            handler(board, cell)
        else:
            # unknown types are skipped but printed for debugging
            print(f"Skipping unknown cell type '{t}' at ({cell.get('row')},{cell.get('col')})")

    return board


def load_level_from_file(path: str) -> Board:
    path = os.path.abspath(path)
    data = read_json_file(path)
    return build_board_from_json(data)