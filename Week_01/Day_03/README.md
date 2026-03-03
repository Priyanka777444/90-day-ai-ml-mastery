# Day 3: Password Generator & Manager

## Features
1. Generate random passwords (customizable length & characters)
2. Save generated passwords with labels
3. Manually save passwords
4. View all passwords (formatted table)
5. Search passwords by label
6. Delete passwords by ID
7. Save all to CSV file
8. Auto-load from CSV on startup

## Concepts Learned
- `random.choices()` for password generation
- `string` module constants
- `''.join()` to convert list to string
- Dictionary field name consistency
- CSV DictWriter/DictReader
- Global variable management

## Bugs Fixed
1. `and` → `or` in validation
2. `break` → proper loop flow
3. Variable name consistency
4. Saving correct variables (gen, pwd vs password list)
5. Field name case matching

## Time Spent
- Learning: 45 min
- Coding: 2.5 hours
- Debugging: 1 hour
- Total: ~4 hours

## AI Code Generated
ZERO. All manual coding.

## Usage
```bash
python password_generator.py