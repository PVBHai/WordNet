from nicegui import ui

a = """
    graph TD
    class.n.08-class["class.n.08-class"]
    class.n.05-class/division["class.n.05-class/division"]
    group.n.01-group/grouping --> people.n.01-people
    class.n.06-class/year["class.n.06-class/year"]
    quality.n.01-quality --> elegance.n.01-elegance
    gathering.n.01-gathering/assemblage --> class.n.02-class/form/grade/course
    taxonomic_group.n.01-taxonomic_group/taxonomic_category/taxon --> class.n.07-class
    gathering.n.01-gathering/assemblage --> class.n.06-class/year
    social_group.n.01-social_group --> gathering.n.01-gathering/assemblage
    class.n.02-class/form/grade/course["class.n.02-class/form/grade/course"]
    biological_group.n.01-biological_group --> taxonomic_group.n.01-taxonomic_group/taxonomic_category/taxon
    class.n.03-class/stratum/social_class/socio-economic_class["class.n.03-class/stratum/social_class/socio-economic_class"]
    people.n.01-people --> class.n.03-class/stratum/social_class/socio-economic_class
    elegance.n.01-elegance --> class.n.08-class
    education.n.01-education/instruction/teaching/pedagogy/didactics/educational_activity --> course.n.01-course/course_of_study/course_of_instruction/class
    course.n.01-course/course_of_study/course_of_instruction/class["course.n.01-course/course_of_study/course_of_instruction/class"]
    association.n.01-association --> league.n.01-league/conference
    collection.n.01-collection/aggregation/accumulation/assemblage --> class.n.01-class/category/family
    class.n.01-class/category/family["class.n.01-class/category/family"]
    league.n.01-league/conference --> class.n.05-class/division
    class.n.07-class["class.n.07-class"]
    activity.n.01-activity --> education.n.01-education/instruction/teaching/pedagogy/didactics/educational_activity
    group.n.01-group/grouping --> collection.n.01-collection/aggregation/accumulation/assemblage
"""

ui.mermaid('''
    graph TD
    +class.n.08-class["class.n.08-class"]
    people.n.01-people --> +class.n.03-class/stratum/social_class/socio-economic_class
    +class.n.1 --> +class.n.2
''')

ui.run()