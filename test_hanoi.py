'''
Created on Feb 15, 2018

@author: SirIsaacNeutron
'''
import unittest
import hanoi

class HanoiTest(unittest.TestCase):
    def test_tower_get_and_remove_smallest_disk(self):
        tower_one = hanoi.Tower(3)
        
        smallest_disk = tower_one._get_and_remove_smallest_disk()     
        self.assertEqual(smallest_disk.size, 1)
        
        next_smallest_disk = tower_one._get_and_remove_smallest_disk()
        self.assertEqual(next_smallest_disk.size, 2)
        
        last_disk = tower_one._get_and_remove_smallest_disk()
        self.assertEqual(last_disk.size, 3)
        
        with self.assertRaises(hanoi.NoDisksError):
            tower_one._get_and_remove_smallest_disk()
            
    def test_basic_hanoi_game(self):
        # Solving the most basic Tower of Hanoi puzzle -- Tower one has
        # just one Disk, so we can move that Disk to Tower three and
        # immediately solve the puzzle.
        game = hanoi.Game(1)
        
        game.tower_one.move_disk_to(game.tower_three)
        self.assertEqual(game.tower_three.get_topmost_disk().size, 1)
        self.assertEqual(game.tower_one[0], hanoi.EMPTY)
        
        self.assertTrue(game.is_over())
        
    def test_more_complex_hanoi_game(self):
        # Solving a Tower of Hanoi puzzle where all Towers can store at 
        # most three Disks.
        game = hanoi.Game(3)
        
        game.tower_one.move_disk_to(game.tower_three)
        game.tower_one.move_disk_to(game.tower_two)
        
        with self.assertRaises(hanoi.InvalidMoveError):
            game.tower_two.move_disk_to(game.tower_three)
        
        # Check if the bottommost Disk has been put back after the
        # invalid move.
        self.assertEqual(game.tower_two.get_topmost_disk().size, 2)
        
        self._make_remaining_moves_for_complex_game(game)
        self.assertTrue(game.is_over())
        
    def _make_remaining_moves_for_complex_game(self, game: hanoi.Game) -> None:
        """Make the last moves necessary to solve the Tower of Hanoi
        puzzle where each Tower has 3 Disks.
        """
        game.tower_three.move_disk_to(game.tower_two)
        game.tower_one.move_disk_to(game.tower_three)
        
        game.tower_two.move_disk_to(game.tower_one)
        game.tower_two.move_disk_to(game.tower_three)
        
        game.tower_one.move_disk_to(game.tower_three)
        
    def test_game_min_moves(self):
        game = hanoi.Game(3)
        self.assertEqual(game.min_moves_required, 7)

    def test_disk_smaller_than(self):
        disk_one = hanoi.Disk(1) 
        disk_two = hanoi.Disk(2)
        self.assertTrue(disk_one.is_smaller_than(disk_two))

        disk_three = hanoi.Disk(1)
        self.assertFalse(disk_one.is_smaller_than(disk_three))
        
if __name__ == '__main__':
    unittest.main()