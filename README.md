# Data Relational Mapping

## Objective

To experiment with an alternative to Object Relational Mapping. On the surface this appears to be a desireable goal because data can be more flexible/composable. It also encourages keeping functionality away from the models themselves. This should allow the models to more accurately represent their domain without being directly aware of real world circumstances. 

It is possible this pattern could be used to address the circular dependencies issue in graphene (more cleanly than it is now). It is also possible that only a small translation layer would be needed to get from graphql to a db query.

Language used to implement isn't important, really. I'd prefer a language w/ interfaces. However, I suspect this pattern has the best chance of showing strenghts in a dynamic language. So the critical choice may be around simplicity of describing the models.

Being able to describe models in something close to json could allow for sharing of details in fat client situations. Having the option could create clients with fat and thin portions.

## (Mostly) Arbitrary choices

* The default should be to query as little as possible. This prevents users from relying on things they aren't asking for.
* `:*` should still be a valid field identifier in a select
* The flow of the sql engine should be very easy to understand so that it is easy to see how it can be extended.

## Model definitions

* A model's definition must only depend on the field types and any validators. These constraints should prevent any need for circular dependancies in the models themselves.
* A type (or fn) that implements a known interface is used as the `:type` value. This allows custom type behavior (like implementing new relationships or serializing types to something suitable for the database). (N.B.: Types may require an interface or map of fns to implement a default validator/options selector)
* Each field may have only one validator function that receives the value of that field.
* Each model may have only one validator function that receives the values of the model.
* Validators do not mutate or transform. They only approve or deny values.
* Models must be registered in some way so the DRM can find the data.
* A model may specify the behavior of it's fk children upon it's deletion (perhaps also on update?) via the chosen fk type.

```clojure
{:model :myModel
 :validator tos-and-created-check
 :fields {:id {:name "id" :type Integer}
          :name {:name "name" :type String :validator (partial max-length-validator 100)}
		  :user-id {:name "user-id" :type OneToOne :model :user}
		  :tos {:name "tos" :type Boolean}}}
```

## Model composition

TODO: In what way should models be composable? Should they even?

## Queries

Queries should flow in a manner similar to graphql. This seems a sensible pattern for mapping the relationship of objects in a graph.

### Query format

```clojure
;; Nested query
{:myModel [:id :created {:user-id {:fields [:id :name]}}]

;; Distinct models as a single query
{:posts [:id :created :tags]
 :activity-summary [:totals]}
 
;; Query with constraints
{:myModel [:id {:created [:greater (yesterday)]}]}
```

TODO: Inserts/Deletes/Updates

### Return format

```clojure
;; Nested response
{:myModel [{:id <id> :created <created> :user-id {:id <id> :name <name>}}]}

;; Distinct model response
{:posts [{:id <id> :created <created> :tags <tags>}{...}{...}]
 :activity-summary [{:totals <totals>}]}
```

## Sql generation

**It is possible this belongs as a separate project, but it seems essential to testing the viability of a DRM**

TODO: Expand

TODO: Detail how the types will return the query maps. It must be suitable for recursive (depth-first?) building.

High level flow:

* Model is found (error if the model isn't registered)
* A map like below is generated
```clojure
{:select [{:from :myModel :fields [:id :created :user-id]}]
 :join [{:users :user-id}]
 :where [[:greater :created <value>][...]]}
```
* Validators are run when appropriate (when is it appropriate)?
* Type serializers run
* Map is parsed into a prepared statement by calling the `:select` fn (etc)
  * This allows for custom join/cte implementations where performance calls for them
* Statement runs and data is returned

## Extension points

### Field types

The field type interface will have `serialize` and `deserialize`. 

`serialize` will prepare data for the database and return it in the proper map. (This seems fucky. Think on it.)

`deserialize` will format the db data for code consumption.

### Validators

A validator will get only a value and return only a boolean. Common validators should be provided, but creating a validator should be common practice.

Validators must not be used to enforce relationships. That is the place of field types. Whole model validators may place constraints that cross fields. (i.e.: If created is after January then tos must be agreed to)

### Sql generation 

TODO: Where will sql generation be extensible so users can call their custom functions? (Likely the `:greater` tag references some code that knows how to build that part of the query)
