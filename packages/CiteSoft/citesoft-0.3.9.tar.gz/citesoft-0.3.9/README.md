CiteSoft_py is a python implementation of CiteSoft. CiteSoft is a plain text standard consisting of a format and a protocol that exports the citations for the  end-users for whichever softwares they have used. CiteSoft has been designed so that software dev-users can rely upon it regardless of coding language or platform, and even for cases where multiple codes are working in a coupled manner.

Can be installed by 'pip install citesoft' which will also install semantic-version ( https://pypi.org/project/semantic-version/ and also PyYAML https://pypi.org/project/PyYAML/)

For the simplest way to learn how to use CiteSoft, open runExample.py then run it.  Then open the two CiteSoft txt files generated (CiteSoftwareCheckpointsLog.txt and CiteSoftwareConsolidatedLog.txt), and also MathExample.py to see what happened.

Basically, when runExample.py is run, citations are generated in a "Checkpoint" file (based on the module that was called and the functions that were called inside MathExample.py). Finally, the citations are consolidated with duplicate entries removed.

There are two types of users of citesoft: dev-users and end-users.

FOR DEV-USERS:
There are are two syntaxes to include citations to their work. The only truly required fields are the unique_id (typically a URL or a DOI) and the software_name. The other valid_optional_fields are encouraged: ["version", "cite", "author", "doi", "url", "encoding", "misc"].  These optional fields are put into kwargs (see MathExample.py for syntax). In this module, all optional fields can be provided as lists of strings or individual strings (such as a list of authors).

1) An "import_cite" which causes a citation to be made when the the module is first imported.
CiteSoft.import_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", write_immediately=True, **kwargs)

2) A "module_call_cite" which causes a citation to be made when a function in the module is actually called. 
@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)

Subsequently, one would use compile_checkpoints_log & compile_consolidated_log (direct CiteSoft module functions), or @CiteSoft.after_call_compile_checkpoints_log & @CiteSoft.after_call_compile_consolidated_log (CiteSoft decorators) to create CiteSoftwareCheckpointsLog.txt and CiteSoftwareConsolidatedLog.txt.

For class-based codes, a logical choice is to use a pair of calls like this before a class's init function:
@CiteSoft.after_call_compile_consolidated_log()
@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def __init__(...)

CiteSoftLocal is NOT a full version of CiteSoft: it is file that only exports Checkpoints and which dev-users can include for distribution with their packages as a 'backup' in case an end-user tries to run the dev-user's package under conditions where CiteSoft or its dependencies are not installed.

FOR END-USERS:
The end-user may find the CiteSoftwareConsolidatedLog.txt to be convenient, but the authoritative list is the list inside CiteSoftwareCheckpoints.txt (though the checkpoint file may include duplicates). The end-user is responsible for citing ALL software used. To facilitate easy of doing so, the dev-user should call the consolidate command when appropriate (such as at the end of a simulation).

A typical CiteSoft entry looks like below (between the 'pre' tags):
<pre>
-
    timestamp: >-
        2020-08-25T11:43:30
    unique_id: >-
        https://docs.python.org/3/library/math.html
    software_name: >-
        The Python Library Reference: Mathematical functions
    version:
        - >-
            3.6.3 
    author:
        - >-
            Van Rossum, Guido
    cite:
        - >-
            Van Rossum, G. (2020). The Python Library Reference, release 3.8.2. Python Software Foundation.
</pre>
