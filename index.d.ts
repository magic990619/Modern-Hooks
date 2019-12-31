// Type definitions for @binteractions/react-hooks
import { MutableRefObject, EffectCallback, DependencyList } from 'react';

export type CallbackSetter = EffectCallback;

// useCallbackRef
export declare const useCallbackRef: () => [MutableRefObject<Function>, EffectCallback];
// useDebouncedCallback
export declare const useDebouncedCallback: (fn: Function, wait?: number, dependencies?: DependencyList) => EffectCallback;
// useGlobalEvent
export declare const useGlobalEvent: (eventName: string) => CallbackSetter;
// useInterval
export declare const useInterval: (delay?: number) => CallbackSetter;
// useLifecycle
export declare const useLifecycle: () => { onMount: CallbackSetter, onUnmount: CallbackSetter };
// useMouseHandler
type MouseTarget = HTMLElement | Document | Window;

type MouseCallbackSetters = {
  onMouseDown: CallbackSetter,
  onMouseEnter: CallbackSetter,
  onMouseLeave: CallbackSetter,
  onMouseMove: CallbackSetter,
  onMouseOut: CallbackSetter,
  onMouseOver: CallbackSetter,
  onMouseUp: CallbackSetter,
}
export declare const useMouseEvents: (ref?: MutableRefObject<MouseTarget>) => MouseCallbackSetters;

// useMouseState
type MouseState = {
  clientX: number,
  clientY: number,
  screenX: number,
  screenY: number,
}
export declare const useMouseState: (ref?: MutableRefObject<MouseTarget>) => MouseState;
// useMouse
export declare const useMouse: (ref?: MutableRefObject<MouseTarget>) => [MouseState, MouseCallbackSetters];

// useOnMount
export declare const useOnMount: () => CallbackSetter;

// usePrev
export declare const usePrev: (value: any) => unknown;

// useThrottledCallback
export declare const useThrottledCallback: (fn: Function, wait?: number, dependencies?: DependencyList) => EffectCallback;

// useTimeout
export declare const useTimeout: (delay?: number) => CallbackSetter;

// useWillUnmount
export declare const useWillUnmount: () => CallbackSetter;
// useWindowResize
export declare const useWindowResize: () => CallbackSetter;
// useWindowScroll
export declare const useWindowScroll: () => CallbackSetter;

// useBatteryEvents

type BatteryCallbackSetters = {
  onChargingChange: CallbackSetter,
  onChangingTimeChange: CallbackSetter,
  onDischargingTimeChange: CallbackSetter,
  onLevelChange: CallbackSetter,
}

export declare const useBatteryEvents: () => BatteryCallbackSetters;

// useBatteryState
type BatteryState = {
  charging: boolean,
  chargingTime: number,
  dischargingTime: number,
  level: number,
}
export declare const useBatteryState: () => BatteryState;
// useBattery
export declare const useBattery: () => [BatteryState, BatteryCallbackSetters];
