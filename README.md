# cloud-formation-echo

## A CloudFormation resource that returns the same string it is supplied with

### Purpose:
This simple plugin is meant to be used as a workaround for the limitations of
[Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).
Specifically, the limitation that the only supported function for the attribute
name is [Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)


### Installation
This custom resource can be installed on your AWS account by deploying the 
CloudFormation template at cloud-formation/cloud-formation.yml, and then 
updating the Lambda function it creates with the code from python/index.py

The Lambda function's ARN, which is needed for use as a service token when
using this custom resource in your CloudFormation  templates, can be found in 
stack's outputs and is registered in
[Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
as
```/cloud-formation/service-tokens/echo```

### Syntax:

The syntax for declaring this resource:

```yaml
MyResource:
  Type: "Custom::EchoSomething"
  Version: "1.0"
  Properties:
    ServiceToken: LAMDA_FUNCTION_ARN
    Echo: "Silly that this even has to be a thing..."
    ...
```
### Properties

#### Service Token
##### The ARN of the Lambda function backing the custom resource

Type: String

Required: Yes

#### Echo
##### The value that the resource should return as its physical resource id

Type: String

Required: Yes

### Return Values

#### Ref
When the logical ID of this resource is provided to the Ref intrinsic function, 
Ref returns the same value that was supplied as the ```Echo``` property
