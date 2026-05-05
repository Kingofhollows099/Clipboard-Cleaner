# A tool helpful for working with spreadsheets! Mainly meant for working with lists, but can be useful for other things as well.
The program works as follows:
1: Imports whatever you have in your clipboard
2: Applies any operations you have enabled
3: Recopies the fixed-up list back to the clipboard.

# Example:
- You copy some text

    Apple, Orange
  
    Bannana
  
    Pineapple (x2)
  
- You click the run button, with all features enabled
- It copies the fixed list back to you clipboard

  Apple
  
  Orange
  
  Bannana
  
  Pineapple

# Available Operations:
### Split on commas
<img width="51" height="62" alt="image" src="https://github.com/user-attachments/assets/9a1b7bbf-fb6b-48f7-aaa6-5bf17b77ab84" />
Seperates comma-seperated values into individual items

Ex: One, Two, Three ->

One

Two 

Three

### Dequantify
<img width="48" height="60" alt="image" src="https://github.com/user-attachments/assets/b82aa592-82af-4622-bff9-831c3514e440" />
Removes quantifiers

Ex: 

Glorp (x50)

Oompta (x10) ->

Glorp

Oompta

### Deduplicate
<img width="48" height="60" alt="image" src="https://github.com/user-attachments/assets/bc4f030b-61b4-4198-a141-1606d7e9d173" />
Removes values that are identical
Ex:

Soda

Soda

Tea

Water ->

Soda

Tea

Water

### Title Case
<img width="48" height="63" alt="image" src="https://github.com/user-attachments/assets/0a5d8e46-6770-4bce-974d-ea142fc39d3d" />
Capitalizes the first letter of each word

Ex:

Not a thing

a thing

kind of a Thing ->

Not A Thing

A Thing

Kind Of A Thing

### Sort Alphabetically
<img width="47" height="60" alt="image" src="https://github.com/user-attachments/assets/6e4971d9-258b-4e82-bdde-c945bec280a4" />
Sorta things alphabetically

Ex:

George

Brandon

Henry ->

Brandon

George

Henry

### Fuzzy match
<img width="128" height="61" alt="image" src="https://github.com/user-attachments/assets/5b2a3a8d-86b9-4690-8477-842a13739e64" />
Helps get rid of typos or small punctuation differences by scanning every list item. The box on the right allows you to adjust the similarity threshold. 

This will cycle through every item in the list, and for each do the following:
- If its similarty value to any item in the unique list is greater than the threshold you have set, merges the new value with the old one.
- If it's similarity threshold is not above the threshold, it adds it to the unique list

Note: This will ignore any list items that contain numbers.
