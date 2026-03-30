declare module "@event-calendar/core" {
  interface ECOptions {
    target: HTMLElement;
    props?: {
      plugins?: Record<string, any>[];
      options?: Record<string, any>;
    };
  }
  export default class EventCalendar {
    constructor(options: ECOptions);
    setOption(name: string, value: any): void;
    getOption(name: string): any;
    getView(): any;
    destroy(): void;
  }
}

declare module "@event-calendar/day-grid" {
  const plugin: { createOptions: Function; createStores: Function };
  export default plugin;
}

declare module "@event-calendar/time-grid" {
  const plugin: { createOptions: Function; createStores: Function };
  export default plugin;
}

declare module "@event-calendar/list" {
  const plugin: { createOptions: Function; createStores: Function };
  export default plugin;
}

declare module "@event-calendar/resource-timeline" {
  const plugin: { createOptions: Function; createStores: Function };
  export default plugin;
}

declare module "@event-calendar/interaction" {
  const plugin: { createOptions: Function; createStores: Function };
  export default plugin;
}
