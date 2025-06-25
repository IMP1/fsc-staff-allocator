## Contents

  - [Overview](#Overview)
  - [Usage](#Usage)
  - [Design](#Design)

## Overview

Staff have various attributes.
Staff have preferences for which camp they're on.
Camps have various criteria for the staff composition: Minimum number of group chiefs with inclusion experience. Minimum number of staff with inclusion experience. All minimum numbers are based on the applications and size of camp and are part of the input to this system.

Some staff have other staff they need to camp with. If one has a higher priority (e.g. is a GC) then they both get allocated according to that priority and that person’s preferences. If not, then the preferences are chosen randomly.
Some staff have other staff they can’t camp with.


## Usage

Takes in a csv file.

Take the `All Applications for All Staff for Summer - First Fortnight.xls` file and save it as a `.csv` file.
The delimiter options are `;` and `|` for the quote-char.

Take the `Camp Requirements - First Fortnight.ods` file and save it as a `.csv` file with the same options.

run `test.py PATH_TO_CAMPS PATH_TO_APPLICATIONS` with the paths to the above files replacing the words in all caps.


## Design


### Assumptions

  - Guaranteed staff members (including camp chiefs, caterers, etc.) and pixie parents are not included in this process, and the required numbers for camps have been adjusted as so.
  - Roughly four fifths of Hodore applicants have inclusion experience, and roughly one quarter of non-Hodore applicants have inclusion experience.
  - Gender doesn’t matter beyond whether or not someone belongs to the gender which is most oversubscribed or not.


### Future Ideas

  - Priority given to those who weren't placed last year
  - 

