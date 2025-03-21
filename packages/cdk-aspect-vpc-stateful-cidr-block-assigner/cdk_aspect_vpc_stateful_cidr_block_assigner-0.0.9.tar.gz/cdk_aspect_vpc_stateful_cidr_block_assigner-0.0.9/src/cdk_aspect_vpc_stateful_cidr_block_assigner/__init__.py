r'''
[![View on Construct Hub](https://constructs.dev/badge?package=cdk-aspect-vpc-stateful-cidr-block-assigner)](https://constructs.dev/packages/cdk-aspect-vpc-stateful-cidr-block-assigner)

# CDK Aspect for VPC Stateful CIDR Block Assignment

Updating Availability Zones (AZs) and subnets in an existing VPC within a deployed CDK stack presents a significant challenge when using the [ec2.Vpc construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html). When introducing new AZs (e.g., from 2 to 3 AZs), CDK attempts to create new subnets for the additional AZ, but these new subnets' CIDR blocks conflict with existing subnet CIDRs. Attempting to do so results in the error message: "The CIDR 'X.Y.Z.0/24' conflicts with another subnet."

The reason is that CDK applications, by design, don't keep state between runs. This means when you try to modify the VPC by adding an AZ, the VPC construct is not aware of what CIDR ranges are already in use from previous deployments.

This project provides a CDK Aspect that alters Amazon VPC subnet CIDR block assignments to respect existing CIDR blocks when updating a CDK VPC construct.

The VpcStatefulCidrBlockAssigner is designed to maintain consistency in VPC subnet CIDR blocks across deployments, ensuring that existing subnets retain their assigned CIDR blocks while allowing for the addition of new subnets.

## Aspect Considerations

**This CDK Aspect does not follow CDK's best practices and is intended as a break-glass solution when the alternatives can't be used.**

Specifically, this CDK Aspect uses a [subnet context file](#generate-subnet-context-file) created by the user as a source of truth for deployed and assigned CIDR blocks. To keep the existing assignments between CIDR Blocks and Subnets, this aspect utilize the [escape hatches](https://docs.aws.amazon.com/cdk/v2/guide/cfn_layer.html) mechanism.

### Preferred Alternatives

* Migrate existing CDK stack to use [VPCv2](https://docs.aws.amazon.com/cdk/api/v2/docs/@aws-cdk_aws-ec2-alpha.VpcV2.html)
* Replace existing CDK stack with a new CDK stack with updated configuration

### Aspect Prerequisites

* VPC construct declares AZs using `availabilityZones` prop and not `maxAzs` prop; E.g., `availabilityZones: ['us-east-1a', 'us-east-1b']`
* You can only apply aspect to a CDK construct tree containing up to one VPC
* VPC construct and provided VPC ID must match

### Limitations

* Only supports IPv4
* One CIDR block per VPC

### General

* To ensure consistency between deployments, you must check in all `${VPC_ID}.subnets.context.json` files to your git repository, see [Generate Subnet Context File](#generate-subnet-context-file)
* Removing this aspect after first use will cause deployment issues

  * Since this CDK aspect overrides the CIDR blocks assigned by the VPC construct, removing this aspect after first use will cause subnets to be assigned their "default" CIDR blocks, resulting in resource replacement or a deployment errors

## General Availability Zone Migration Considerations

When migrating AWS resources between AZs, it's recommended to use the Expand/Shrink approach. This method involves expanding your VPC to include new AZs, deploy your application resources in the new AZs, and then gradually shrink the footprint in the AZs you want to migrate away from.

The shrinking process, which involves removing resources and subnets from the AZs you're migrating away from, requires extreme caution. Before deleting any AWS resources or subnets, it's essential to ensure that all critical workloads and data have been successfully migrated to the new AZs. Only after confirming that all resources have been safely migrated and that there are no dependencies on the old AZs should you proceed with deletion. Remember that deleting resources is irreversible, so always double-check and consider using temporary safeguards like disabling termination protection only when you're absolutely certain about the deletion.

## Usage Instructions

### Installation

Prerequisites:

* Node.js (v14 or later)
* AWS CDK v2.177.0 or compatible version

To install the package in your project:

```bash
npm install cdk-aspect-vpc-stateful-cidr-block-assigner
```

### Generate Subnet Context File

The VpcStatefulCidrBlockAssigner relies on a JSON file describing the current state of your VPC. The users are responsible for creating and updating this file before and after any change to their VPC state. To be aligned with CDK's terminology we refer to this file as the subnet context file.

This file should be named `{vpcId}.subnets.context.json` and placed in the project root or the specified `contextFileDirectory`.

The subnet context file holds a list of JSON objects describing each subnet inside a VPC:

```json
[
    {
        "Name": "SubnetName",
        "AvailabilityZone": "AvailabilityZone",
        "CidrBlock": "SubnetCidrBlock"
    },
    ...
]
```

This CDK aspect will try to use the values in the subnet context file to match between subnets and CIDR blocks during CDK synth time to prevent CIDR block conflicts when introducing or replacing VPC AZs.

I highly recommend to create and update this file manually only. Do not set up any automation around it since any changes done to your VPC should be done carefuly and responsibly, with high level of awareness.

To generate this file, use the following AWS CLI command:

```bash
export VPC_ID="{VPC ID}"
aws ec2 describe-subnets --filters Name=vpc-id,Values=${VPC_ID} --query "Subnets[*].{Name: Tags[?Key == 'aws-cdk:subnet-name'] | [0].Value, AvailabilityZone: AvailabilityZone, CidrBlock: CidrBlock}" > ${VPC_ID}.subnets.context.json
```

Replace `{VPC ID}` with your actual VPC ID.

### Getting Started

1. Import the VpcStatefulCidrBlockAssigner in your CDK stack:

```python
import { VpcStatefulCidrBlockAssigner } from 'cdk-aspect-vpc-stateful-cidr-block-assigner';
import * as cdk from 'aws-cdk-lib';
```

1. Apply the aspect to your VPC construct:

```python
const network = new Network(this, 'Network', {
  // ... your network construct configuration, this construct must contain up to one VPC construct
});


const vpcStatefulCidrBlockAssigner = new VpcStatefulCidrBlockAssigner({
  vpcId: 'vpc-01234567890abcdef'
});
cdk.Aspects.of(network).add(vpcStatefulCidrBlockAssigner, {
  priority: cdk.AspectPriority.MUTATING
});
```

The `priority: cdk.AspectPriority.MUTATING` option informs CDK this Aspect mutates the construct tree, and needs to be invoked before any readonly Aspects which are commonly used for security validations before deployment. E.g., [cdk-nag](https://github.com/cdklabs/cdk-nag).

### Configuration Options

The `VpcStatefulCidrBlockAssigner` accepts the following properties:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| vpcId | string | The ID of the VPC you want to manage. | 'vpc-01234567890abcdef' |
| contextFileDirectory | string (optional) | Custom directory path for the subnet context file. | 'path/to/context/' |
| availabilityZoneSubstitutions | Array<AvailabilityZoneSubstitution> (optional) | An array of AZ substitutions for reassigning CIDR blocks. | [{ source: 'us-east-1a', target: 'us-east-1b' }, { source: 'us-east-1c', target: 'us-east-1d' }] |

Example with all options:

```python
const vpcStatefulCidrBlockAssigner = new VpcStatefulCidrBlockAssigner({
  vpcId: 'vpc-01234567890abcdef',
  contextFileDirectory: 'path/to/context/',
  availabilityZoneSubstitutions: [
    { source: 'us-east-1a', target: 'us-east-1b' },
    { source: 'us-east-1c', target: 'us-east-1d' },
  ]
});
```

### Supported Actions

The VPC construct assigns [Logical IDs](https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html#identifiers_logical_ids) to its subnets based on the order of `availabilityZones`. Any change to these Logical ID will cause a re-deployment of the resource.

Adding or removing AZs in the non-last spot of `availabilityZones` will cause a re-arrangement of the AZ order, which in turn, cause changes to the subnets' Logical IDs and a replacement.

#### Add Availability Zones

To add a new Availability Zone to your VPC:

1. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file
2. Update your VPC configuration in your CDK stack to include the new AZ in the `availabilityZones` prop
3. Ensure the new AZ is added as the last (right-most) item in the `availabilityZones` array
4. [Optional] Use `npx cdk diff` command to inspect the upcoming changes
5. Run your CDK deployment command (e.g., `npx cdk deploy`)
6. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file

Example:

```python
const vpc = new ec2.Vpc(this, 'MyVpc', {
  ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
  availabilityZones: ['us-east-1a', 'us-east-1b', 'us-east-1c'], // Added 'us-east-1c'
  // ... other configuration options
});
```

The VpcStatefulCidrBlockAssigner will automatically assign CIDR blocks to the new subnets in the added AZ while preserving the existing CIDR block assignments for the other AZs.

#### Remove Availability Zones

To remove an Availability Zone from your VPC:

1. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file
2. Make sure there are no AWS resources depending on subnets in the deleted AZs
3. Update your VPC configuration in your CDK stack to remove the AZ from the `availabilityZones` prop
4. Ensure you are only removing the last (right-most) AZ from the `availabilityZones` array
5. [Optional] Use `npx cdk diff` command to inspect the upcoming changes
6. Run your CDK deployment command (e.g., `npx cdk deploy`)
7. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file

Example:

```python
const vpc = new ec2.Vpc(this, 'MyVpc', {
  ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
  availabilityZones: ['us-east-1a', 'us-east-1b'], // Removed 'us-east-1c'
  // ... other configuration options
});
```

The VpcStatefulCidrBlockAssigner will automatically handle the removal of subnets in the deleted AZ while maintaining the CIDR block assignments for the remaining AZs.

#### Substitute Availability Zones

When AWS CloudFormation performs a replacement of an AWS resource it first deploys the new resource and then deletes the old resource. When substituting between AZs we want to re-use existing CIDR blocks, hence, we need to manually delete the subnets in the AZs we are substituting "to free up" the CIDR blocks for the new subnets.

Note: This diverges from IaC best practices and should be done with extreme caution.

To substitute one Availability Zone with another:

1. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file
2. Update your VPC configuration in your CDK stack to replace the old AZ with the new one in the `availabilityZones` prop
3. Configure the VpcStatefulCidrBlockAssigner with the `availabilityZoneSubstitutions` option
4. Manually delete the subnets in the removed AZs
5. [Optional] Use `npx cdk diff` command to inspect the upcoming changes
6. Run your CDK deployment command (e.g., `npx cdk deploy`)
7. Remove the `availabilityZoneSubstitutions` option from VpcStatefulCidrBlockAssigner
8. Follow [Generate Subnet Context File](#generate-subnet-context-file) instructions to generate an updated subnet context file

Example:

```python
const vpc = new ec2.Vpc(this, 'MyVpc', {
  ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
  availabilityZones: ['us-east-1c', 'us-east-1b'], // Replaced 'us-east-1a' with 'us-east-1c'
  // ... other configuration options
});

const vpcStatefulCidrBlockAssigner = new VpcStatefulCidrBlockAssigner({
  vpcId: 'vpc-01234567890abcdef',
  availabilityZoneSubstitutions: [
    { source: 'us-east-1b', target: 'us-east-1c' }
  ]
});

cdk.Aspects.of(vpc).add(vpcStatefulCidrBlockAssigner);
```

The VpcStatefulCidrBlockAssigner will reassign the CIDR blocks from the old AZ (us-east-1a) to the new AZ (us-east-1c) while maintaining the existing CIDR block assignments for other AZs.

### Example Migration Plan

Starting point: `availabilityZones: ['us-east-1a', 'us-east-1b']`
Goal: `availabilityZones: ['us-east-1a', 'us-east-1c']`
Requirement: Always have at least two active AZs

1. Expand by adding a new temporary 'non-goal' AZ: `availabilityZones: ['us-east-1a', 'us-east-1b', 'us-east-1d']`

   1. Deploy the application to the new AZ (us-east-1d)
   2. Test that the application is stable
2. Substitute original AZ with a goal AZ: `availabilityZones: ['us-east-1a', 'us-east-1c', 'us-east-1d']`

   1. Deploy the application to the new AZ (us-east-1c)
   2. Test that the application is stable
3. Shrink temporary 'non-goal' AZ: `availabilityZones: ['us-east-1a', 'us-east-1c']`

   1. Test that the application is stable

## CIDR Block Assignment Flow

CDK aspects are a powerful feature that allow you to apply cross-cutting changes to your CDK constructs. They work by implementing the `IAspect` interface, which defines a `visit` method. This method is called for each construct in the construct tree, allowing the aspect to inspect and modify the constructs as needed. The VpcStatefulCidrBlockAssigner uses this mechanism to intercept and modify subnet CIDR block assignments, ensuring consistency across deployments while respecting existing assignments.

```mermaid
flowchart TD;
   Visit-->IsSubnet{Is it a Subnet?};
   IsSubnet-->NotSubnet[Not a subnet, exit];
   IsSubnet-->IsExistingSubnet{Is it an existing subnet?};
   IsExistingSubnet-->ExistingSubnet[Yes, assign CIDR block from Subnet context];
   IsExistingSubnet-->NewSubnet[No, Assign a fresh CIDR block];
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-aspect-vpc-stateful-cidr-block-assigner.AvailabilityZoneSubstitution",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target"},
)
class AvailabilityZoneSubstitution:
    def __init__(self, *, source: builtins.str, target: builtins.str) -> None:
        '''Represents a mapping between source and target Availability Zones for subnet substitution.

        :param source: The source Availability Zone to substitute from. All subnets in this AZ must be manually deleted before substitution.
        :param target: The target Availability Zone to substitute to. The source AZ's subnet CIDR blocks will be assigned to subnets in this AZ.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee18c6b5956ae3a547b04e8b95e1dae3b3b8e09c6fa6804a2f0a086b76b4b06)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }

    @builtins.property
    def source(self) -> builtins.str:
        '''The source Availability Zone to substitute from.

        All subnets in this AZ must be manually deleted before substitution.

        Example::

            'us-east-1a'
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''The target Availability Zone to substitute to.

        The source AZ's subnet CIDR blocks will be assigned to subnets in this AZ.

        Example::

            'us-east-1b'
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AvailabilityZoneSubstitution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class VpcStatefulCidrBlockAssigner(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aspect-vpc-stateful-cidr-block-assigner.VpcStatefulCidrBlockAssigner",
):
    '''An aspect which can be applied to a VPC to override CIDR blocks of subnets.

    This aspect rely on a Subent context file containing an updated data about your deployed VPC structure.
    To generate this file, use the script in README.md.
    The default location for the Subnet context file is at Current Working Directory.

    Example::

        const network = Network(...) // Contains exactly one VPC construct
        
        const vpcStatefulCidrBlockAssigner = new VpcStatefulCidrBlockAssigner({
          vpcId: 'vpc-01234567890abcdef'
        });
        cdk.Aspects.of(network).add(vpcStatefulCidrBlockAssigner, {
          priority: cdk.AspectPriority.MUTATING
        });
    '''

    def __init__(
        self,
        *,
        vpc_id: builtins.str,
        availability_zone_substitutions: typing.Optional[typing.Sequence[typing.Union[AvailabilityZoneSubstitution, typing.Dict[builtins.str, typing.Any]]]] = None,
        context_file_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_id: The VPC ID for the updated VPC. This VPC ID will be used to locate the Subnet context file on the filesystem.
        :param availability_zone_substitutions: An optional mapping of Availability Zones to substitute. Used to assign the source AZ's subnets' CIDR blocks for the target AZ's subnets. You must first manually delete all VPC subnets in each of the source AZs.
        :param context_file_directory: An optional directory path for the Subnet context file. When specifiying ``contextFileDirectory``, the Subnet context file will be looked for at ``{contextFileDirectory}/{vpcId}.subnets.context.json``
        '''
        props = VpcStatefulCidrBlockAssignerProps(
            vpc_id=vpc_id,
            availability_zone_substitutions=availability_zone_substitutions,
            context_file_directory=context_file_directory,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd7260085fde7daeec29ccc0578f59c3d6b6b5f6fb59b40e998d6c11a709839)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="cdk-aspect-vpc-stateful-cidr-block-assigner.VpcStatefulCidrBlockAssignerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_id": "vpcId",
        "availability_zone_substitutions": "availabilityZoneSubstitutions",
        "context_file_directory": "contextFileDirectory",
    },
)
class VpcStatefulCidrBlockAssignerProps:
    def __init__(
        self,
        *,
        vpc_id: builtins.str,
        availability_zone_substitutions: typing.Optional[typing.Sequence[typing.Union[AvailabilityZoneSubstitution, typing.Dict[builtins.str, typing.Any]]]] = None,
        context_file_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_id: The VPC ID for the updated VPC. This VPC ID will be used to locate the Subnet context file on the filesystem.
        :param availability_zone_substitutions: An optional mapping of Availability Zones to substitute. Used to assign the source AZ's subnets' CIDR blocks for the target AZ's subnets. You must first manually delete all VPC subnets in each of the source AZs.
        :param context_file_directory: An optional directory path for the Subnet context file. When specifiying ``contextFileDirectory``, the Subnet context file will be looked for at ``{contextFileDirectory}/{vpcId}.subnets.context.json``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f787582a4379694136851b4ac26f05184a028c37f2bc85bbf8ed6c0b38a371cb)
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument availability_zone_substitutions", value=availability_zone_substitutions, expected_type=type_hints["availability_zone_substitutions"])
            check_type(argname="argument context_file_directory", value=context_file_directory, expected_type=type_hints["context_file_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_id": vpc_id,
        }
        if availability_zone_substitutions is not None:
            self._values["availability_zone_substitutions"] = availability_zone_substitutions
        if context_file_directory is not None:
            self._values["context_file_directory"] = context_file_directory

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The VPC ID for the updated VPC.

        This VPC ID will be used to locate the Subnet context file on the filesystem.

        Example::

            'vpc-01234567890abcdef'
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone_substitutions(
        self,
    ) -> typing.Optional[typing.List[AvailabilityZoneSubstitution]]:
        '''An optional mapping of Availability Zones to substitute.

        Used to assign the source AZ's subnets' CIDR blocks for the target AZ's subnets.
        You must first manually delete all VPC subnets in each of the source AZs.

        :throws: Error if a source Availability Zone is found in the VPC

        Example::

            [
              {source: 'us-east-1a', target: 'us-east-1b'},
              {source: 'us-east-1c', target: 'us-east-1d'},
            ]
        '''
        result = self._values.get("availability_zone_substitutions")
        return typing.cast(typing.Optional[typing.List[AvailabilityZoneSubstitution]], result)

    @builtins.property
    def context_file_directory(self) -> typing.Optional[builtins.str]:
        '''An optional directory path for the Subnet context file.

        When specifiying ``contextFileDirectory``, the Subnet context file will be looked for at ``{contextFileDirectory}/{vpcId}.subnets.context.json``

        Example::

            'path/to/context/'
        '''
        result = self._values.get("context_file_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcStatefulCidrBlockAssignerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AvailabilityZoneSubstitution",
    "VpcStatefulCidrBlockAssigner",
    "VpcStatefulCidrBlockAssignerProps",
]

publication.publish()

def _typecheckingstub__2ee18c6b5956ae3a547b04e8b95e1dae3b3b8e09c6fa6804a2f0a086b76b4b06(
    *,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd7260085fde7daeec29ccc0578f59c3d6b6b5f6fb59b40e998d6c11a709839(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f787582a4379694136851b4ac26f05184a028c37f2bc85bbf8ed6c0b38a371cb(
    *,
    vpc_id: builtins.str,
    availability_zone_substitutions: typing.Optional[typing.Sequence[typing.Union[AvailabilityZoneSubstitution, typing.Dict[builtins.str, typing.Any]]]] = None,
    context_file_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
