# Client Architecture (Front-End)

## Tech Stack
- **Framework**: React (Vite)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (Optional) or Plain CSS with Modules.
    - *Decision*: Plain CSS or CSS Modules for "Premium" look without extra deps if user didn't ask for Tailwind. The system prompt says "Use Vanilla CSS... Avoid using TailwindCSS unless USER explicitly requests it".
    - But for a "Premium" look, I might want some utility classes. I'll stick to Vanilla CSS with a strong design system in `index.css`.

## Components
1.  **Layout**: Main container with Header and Footer.
2.  **SplitEditor**: Left side = Java Input (Monaco Editor or Textarea), Right side = Playwright Output (Monaco/Readonly).
3.  **Controls**: "Convert" button, "Clear" button, "Settings" button.
4.  **FileViewer**: Tabbed interface for output files (Page Objects, Specs).

## State Management
- `useConversion`: Custom hook to manage input, loading state, and response data.

## API Integration
- `api/client.ts`: Wrapper for `fetch('http://localhost:3001/api/convert')`.
