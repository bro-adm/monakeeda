# monakeeda
Simple Data Classes implemented with SOLID standards (entensible, readable, ... :)

# Desing

## SOLID Based

...

## Design Questions

### Initilazation per field or per components list?

Just to understand, this is not saying that the MainCompoentns will not run in the order they are provided, it is saying thattheir inner components will run freely according to their discovery order or via field order.

Lets look at the discovery for each main component:
* Fields/Annotations -> discovered according to __annotations__ keys order
* Decorators -> discovered by going over class attrs and finding attrs with  teh decorated_with landscape
* Config -> Does not have direct effects on a specific field. Additional components creqated via the Config cls will be appended to a standard run order

These discovered components order is the order they will run if not managed by a for loop on fields (via __annotations__ keys).
This being said, we can undestand that no native component needs the extra validation that it runs by a managed keys for loop.

### Priority setup?

...

### Build validation or landscape setup -> what runs first?

Logically and naming thinking would lead you to the obvious solution of running validation and then setup.
But after deciding on a set scopes for each of these operations I changed my mind.

Here is the operations scope for the model pipeline (currently not in any particular order):
* init -> The model is already set with all the model client built configurations, now its just the matter of alowing the composite components to run their values_handlers to act out the wanted operations on the model instance values
* setup_landscape -> For simple components it just a matter to add some landscapes to the model cls with the client configurations of the components (but without actually carring for the configurations provided. For CompositeComponent it is to run its nested components landscape setup. For MainComponents it is to find their nested components according to bases and the class pythonic features and then running their landscape setups. Again this happens without carring for what the compoents where configured with.
* validation -> Validates the components client configurablbe aspects (like parameters)

There is no point for setting up all the landscapes without validating the configurable componets where setup properly.
On a completly seperate set of hands, lets think about the MainComponent again.
If it wants to fit in the component api (which it does) whilst still having the responsibility to find the nested components (landscape setup responsibility), it will need to run the landscape_setup before the validations.

In a simpler world this would notify me that the MainComponent is not actually a Component or that I need to implement a order swith to the build method.
In fact running the setup before validation will just make it take more time to get to the raise the validation error if their is one.
But if you think about it the validation is only relevant to verify that the proggrammer that created the class itself set it up properly. In other words only for DEV runtime and in PROD it shouldnt even need to run (saves time).

This in fact is why the PROD/DEV deifferntial exists, along with allowing me to implemnt setup before validations.

### Extra Notes?

Certainly, as long as implementations stay within the scopes of they opeartions no issue should be raised from this design (hopefully :) 
