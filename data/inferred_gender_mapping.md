The file `inferred_gender_mapping.csv` records the gender of people that served in the various invited capacities in the conferences. Gender is inferred from first name and country using genderize.io.

### Field description

The file holds a mapping between names and genders as follows:

 * `name` (string): The normalized name of a person.
 * `gender` (F/M categorical string): One letter denoting gender for female or male.
 * `probability` (numeric, optional): Confidence level for inference, as computed by genderize.io
