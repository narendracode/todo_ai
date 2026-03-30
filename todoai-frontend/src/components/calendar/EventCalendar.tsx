"use client";
import { useEffect, useRef } from "react";
import { useAppDispatch } from "@/store/hooks";
import { setVisibleRange } from "@/store/slices/calendarSlice";
import { calendarApi } from "@/lib/api/calendar";
import "@event-calendar/core/index.css";

// @event-calendar/core is a vanilla JS library — use a DOM ref, not JSX rendering
export function EventCalendar() {
  const dispatch = useAppDispatch();
  const containerRef = useRef<HTMLDivElement>(null);
  const calendarRef = useRef<any>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let destroyed = false;

    Promise.all([
      import("@event-calendar/core"),
      import("@event-calendar/day-grid"),
      import("@event-calendar/time-grid"),
      import("@event-calendar/list"),
      import("@event-calendar/resource-timeline"),
      import("@event-calendar/interaction"),
    ]).then(([core, dayGrid, timeGrid, list, resourceTimeline, interaction]) => {
      if (destroyed || !containerRef.current) return;

      const EC = core.default;

      calendarRef.current = new EC({
        target: containerRef.current,
        props: {
          plugins: [
            dayGrid.default,
            timeGrid.default,
            list.default,
            resourceTimeline.default,
            interaction.default,
          ],
          options: {
            view: "dayGridMonth",
            headerToolbar: {
              start: "prev,next today",
              center: "title",
              end: "dayGridMonth,timeGridWeek,timeGridDay,listWeek,resourceTimelineWeek",
            },
            height: "calc(100vh - 8rem)",
            datesSet: async (info: { start: Date; end: Date }) => {
              try {
                const res = await calendarApi.getEvents(
                  info.start.toISOString(),
                  info.end.toISOString()
                );
                calendarRef.current?.setOption("events", res.data);
                dispatch(
                  setVisibleRange({
                    start: info.start.toISOString(),
                    end: info.end.toISOString(),
                  })
                );
              } catch {
                // backend unavailable
              }
            },
          },
        },
      });
    });

    return () => {
      destroyed = true;
      calendarRef.current?.destroy?.();
      calendarRef.current = null;
    };
  }, [dispatch]);

  return (
    <div className="h-full">
      <style>{`
        .ec {
          --ec-border-color: hsl(214.3 31.8% 91.4%);
          --ec-today-bg-color: hsl(210 40% 96.1%);
          font-family: inherit;
        }
      `}</style>
      <div ref={containerRef} />
    </div>
  );
}
