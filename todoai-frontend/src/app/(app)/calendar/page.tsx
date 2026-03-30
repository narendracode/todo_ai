import { EventCalendar } from "@/components/calendar/EventCalendar";

export default function CalendarPage() {
  return (
    <div className="p-6 h-full">
      <h1 className="text-2xl font-bold mb-4">Calendar</h1>
      <EventCalendar />
    </div>
  );
}
