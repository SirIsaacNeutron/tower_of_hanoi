'''
A console version of Tower of Hanoi.
Created on Feb 19, 2018

@author: SirIsaacNeutron
'''
import hanoi


def _get_game() -> hanoi.Game:
    """Ask the user how many Disks per Tower that he wants, and
    return a Game object with that many Disks per Tower.
    """
    while True:
        num_disks_per_tower = input('How many Disks per Tower do you want?\n')
        try:
            num_disks_per_tower = int(num_disks_per_tower)
            game = hanoi.Game(num_disks_per_tower)
            return game
        except ValueError:
            print('Error: please type in a whole number.')


def _determine_if_user_wants_help_message() -> None:
    """Print a help message if the user so desires, else do nothing."""
    while True:
        yes_or_no = input('Do you want to see instructions on how to play '
                          + 'Tower of Hanoi? (Type yes or no)\n')
        
        if yes_or_no.startswith('y') or yes_or_no.startswith('Y'):
            _print_help_message()
            break
        elif yes_or_no.startswith('n') or yes_or_no.startswith('N'):
            break
        else:
            print("Error: must type 'yes' or 'no'")
  
    
def _print_help_message() -> None:
    """Print the instructions for Tower of Hanoi."""
    print('Welcome to the Tower of Hanoi program!')
    print(('Your goal is to get all the Disks from the leftmost Tower to '
           + 'the rightmost.'))
    print('Rules:')
    print('\t1. You can only move one Disk at a time.')
    print('\t2. You can only remove the topmost Disk from any Tower.')
    print(('\t3. For a Disk to be on top of another Disk, the top Disk has '
           + 'to smaller than the bottom Disk.'))
    print("\t    For example, a Disk with size 3 CAN'T be on top of a Disk of "
          + 'size 2, or a Disk of size 1.')
    print('\t    A Disk with size 3 CAN be on top of a Disk of size 4 '
          + 'or more.')
    print('\t4. When you move a Disk into another Tower, the Disk falls down '
          + 'as far as possible.')
    print("Disk sizes are represented by numbers. [1] means "
          + "'A Disk with size 1.'")
    print("[ ] means 'This spot is empty.'")
    print()
  
      
def _update_game(game: hanoi.Game) -> hanoi.Game:
    """Update the status of the game and return a Game object reflecting
    the current status of the game after making a move.
    """
    original_tower, new_tower = _get_towers_involved_in_move()
    
    # This dict allows us to avoid several if-statements checking
    # what original_tower and new_tower are.
    TOWER_DICT = {'1': game.tower_one, '2': game.tower_two,
                  '3': game.tower_three}
    try:
        if original_tower == new_tower:
            print('Move canceled.')
            return game
        TOWER_DICT[original_tower].move_disk_to(TOWER_DICT[new_tower])
        game.num_moves_made += 1
    except hanoi.InvalidMoveError:
        print('Error: Invalid move! Disks must always be smaller than '
              + 'the Disks they are on top of.')
    except hanoi.NoDisksError:
        print('Error: No Disks in a Tower you specified.')
    except hanoi.InvalidFirstMoveError:
        print('Error: Your first move must be from Tower 1!')
    return game


def _get_towers_involved_in_move() -> (str, str):
    """Return a 2-tuple where the first element is the Tower we are
    moving from, and the second element the Tower we are moving to.
    """
    while True:
        original_tower = input('From which Tower do you want to move a Disk? '
                               + '(e.g., 1)\n')
        
        if original_tower not in ('1', '2', '3'):
            print('Error: you must type 1, 2, or 3 to refer to Towers.')
            continue
        
        new_tower = input('Which Tower are you moving the Disk to? '
                          + '(e.g., 2)\n')
            
        if new_tower not in ('1', '2', '3'):
            print('Error: you must type 1, 2, or 3 to refer to Towers.')
            continue
        break
    return (original_tower, new_tower)

  
if __name__ == '__main__':
    game = _get_game()
    _determine_if_user_wants_help_message()
    
    while not game.is_over():
        game.print_towers()
        game = _update_game(game)
                
    game.print_towers()
    print('Congratulations, you solved the puzzle!')
    print('Minimum number of moves required:', game.min_moves_required)
    print('Number of moves you made:', game.num_moves_made)
    