# yolo.py
extensible and scalable discord bot template

A bot that primarily runs off the given `config.json` which allows for assigning permissions to given commands and automatically allows the main file to locate the command (based off `config['commands_folder']`).
Any commands must be placed in the corresponding commands folder with a name relating to that of which is defined within the configuration's command permissions e.g. `test.py` for a `test: ["@everyone"]` and thus an asynchronous function (`async def` declaration) which has the name definition of that which is in the configuration, and the name of the file (minus the extension).

Because of the nature of this design, you can define as many (so-called) hidden functions which are not accessed by the main caller but are available to be called by the callee/command:

```py
async def print_init():
  print("hey!")

async def test(**kwargs):
  await print_init()
  ...
```

A thing to note is the keyword argument `**kwargs` which has to always be defined within the definition of the function as so the caller can pass arguments such as the bot, the message and the configuration (sans token) to the command so that code repetition is not needed and data can be shared evenly.

A possible issue might arise as the configuration may store any form of superfluous/user-provided data thus a privacy issue is clearly present because the interpassing of the configuration will negate any form of data protection.

However, standardly, a command module shan't have need to access or misuse unrelated configuration data, however it is a thing to be kept in mind. If further data protection is required, then a developer can just pop data that the callee willn't use per another addition unto the configuration such as a `callee_acl` defined perhaps like this:

```json
{
  ...
  "callee_acl": {
    "test": ["certain_data_test_needs"],
    "foo": ["certain_data_foo_needs"]
  },
  
  ...
  
  "certain_data_foo_needs": "...",
  "certain_data_test_needs": "..."
}
```

And so minimal data protection is incorporated, pedantically-speaking, the callee can still read the data innately from the configuration file as the name is bound to be predefined as `config.json` which may thus concern the protection.
