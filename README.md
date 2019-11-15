# IKEA TRADFRI REMOTE

### An AppDaemon app to control lights and scenes with a Zigbee2MQTT connected TRÅDFRI remote

## E1524/E1810 remote (the round one):

| button |  |
|------------|----------------------------------------------------------------------------|
| power | toggle the state of the currently selected group |
| brightness up / down | change the brightness of the currently selected group |
| brightness up + power | set the brightness to 100% |
| brightness down + power | set the brightness to 1% |
| left arrow | cycle between groups |
| right arrow | turn on the next scene to all the groups (without turning on the lights which are switched off) |
| hold power | turn on/off all the groups |

## E1743 dimmer:

| button |  |
|------------|----------------------------------------------------------------------------|
| on | toggle the state of the currently selected group |
| off | cycle between groups |
| hold on | change the brightness of the currently selected group |
| hold off | turn on the next scene to all the groups (without turning on the lights which are switched off) |

## Configuration example

This should be pasted in appdaemon/apps.yaml
```
remote_1:
  module: real_tradfri_remote
  class: TradfriRemote
  groups:
    group_1:
      - light.kitchen_ceiling_1
      - light.kitchen_ceiling_2
    group_2:
      - light.kitchen_spotlights
    group_3:
      - light.kitchen_led_strip
  scenes: input_select.kitchen_mood
  hold_group: group.kitchen
  remote: sensor.tradfri_remote_click
```

| key | value |
|------------|----------------------------------------------------------------------------|
| groups | a map of all the groups, each group is a list of lights |
| scenes | an input_select entity id, it cycles between the options |
| hold_group | a group to switch on/off when holding the power button |
| remote | tradfri remote's zigbee2mqtt entity (e.g. sensor.0xccccccfffe4062b9_click) |

## HACS installation

- Install AppDaemon, if you are on Hass.io you can use the add-on
- Add `https://github.com/notherealmarco/ha-tradfri-remote` custom repository (AppDaemon category)
- Paste the configuration at the end of the `appdaemon/apps.yaml`

## Manual installation

- Install AppDaemon, if you are on Hass.io you can use the add-on
- Clone or download the repo
- Paste `real_tradfri_remote` (`apps/real_tradfri_remote`) in `appdaemon/apps directory`
- Paste the configuration at the end of the `appdaemon/apps.yaml`