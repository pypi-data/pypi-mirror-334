from .decoders import Decoders
from .identifier import Identifier
from .register import Register
from .sources import Sources
from .transformations import Transformations
from .type import Type


class RegisterFactory:
    @staticmethod
    def version(identifier: Identifier) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.VERSION,
            address=0x0000,
            decoder=Decoders.INT_16,
            transformation=Transformations.IDENTITY,
            type=None,
        )

    @staticmethod
    def last_error(identifier: Identifier) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.LAST_ERROR,
            address=0x0000,
            decoder=Decoders.ERROR,
            transformation=Transformations.IDENTITY,
            type=Type.ERROR,
        )

    @staticmethod
    def front_panel_switch(identifier: Identifier, address: int) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.FRONT_PANEL,
            address=address,
            decoder=Decoders.INT_16,
            transformation=Transformations.IDENTITY,
            type=Type.SWITCH,
        )

    @staticmethod
    def system_temperature(identifier: Identifier, address: int, is_writtable: bool = False) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.SYSTEM,
            address=address,
            decoder=Decoders.INT_16,
            transformation=Transformations.NUMERIC_ONE_TENTH,
            type=Type.TEMPERATURE,
            is_writtable=is_writtable,
        )

    @staticmethod
    def system_unitless(identifier: Identifier, address: int, is_writtable: bool = False) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.SYSTEM,
            address=address,
            decoder=Decoders.INT_16,
            transformation=Transformations.NUMERIC_ONE_TENTH,
            type=Type.UNITLESS,
            is_writtable=is_writtable,
        )

    @staticmethod
    def system_switch(identifier: Identifier, address: int) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.SYSTEM,
            address=address,
            decoder=Decoders.INT_16,
            transformation=Transformations.IDENTITY,
            type=Type.SWITCH,
        )

    @staticmethod
    def system_hours(identifier: Identifier, address: int) -> Register:
        return Register(
            identifier=identifier,
            source=Sources.SYSTEM,
            address=address,
            decoder=Decoders.INT_16,
            transformation=Transformations.IDENTITY,
            type=Type.HOURS,
        )
