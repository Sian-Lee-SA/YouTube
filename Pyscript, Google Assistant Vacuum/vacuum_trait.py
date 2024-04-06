from homeassistant.components.google_assistant.trait import (
    StartStopTrait as _StartStopTrait,
    register_trait,
    TRAITS,
    COMMAND_STARTSTOP
)
from homeassistant.components import (vacuum)


TRAITS.remove(_StartStopTrait)
@register_trait
class StartStopTrait(_StartStopTrait):

  
    def sync_attributes(self):
        """Return StartStop attributes for a sync request."""
        attr = super().sync_attributes()
        if self.state.domain == vacuum.DOMAIN and self.state.attributes.get('rooms', False):
            attr["availableZones"] = list(self.state.attributes.get('rooms').keys())

        return attr

    
    async def execute(self, command, data, params, challenge):
        """Execute a StartStop command."""
        domain = self.state.domain
        if domain == vacuum.DOMAIN and command == COMMAND_STARTSTOP and params["start"]:
            if "zone" in params or "multipleZones" in params:
                zones = []
                if "multipleZones" in params:
                    zones = params["multipleZones"]
                else:
                    zones.append(params["zone"])

                return await self.hass.services.async_call(
                    'script',
                    'roborock_clean_by_rooms',
                    {
                        'rooms': zones
                    },
                    blocking=True,
                    context=data.context,
                )

        return await super().execute(command, data, params, challenge)
