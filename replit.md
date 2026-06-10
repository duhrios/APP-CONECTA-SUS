# Sistema SUS - Check-in Application

## Overview

This is a healthcare check-in system designed for the Brazilian Unified Health System (SUS) in São Paulo. The application enables patients to check in at health units using geolocation verification, receive queue numbers, and track their position in the waiting line. The system validates patient proximity to health facilities before allowing check-ins and manages a virtual queue with real-time position tracking.

## Recent Changes

**November 7, 2025**:
- Increased initial check-in distance validation from 5km to 10km based on user request
- Implemented automatic queue advancement (simulates patient processing every 60 seconds)
- Added safeguards to prevent premature queue advancement by resetting timer when first patient enters
- Enhanced location validation at position 3: now explicitly cancels check-in if geolocation data is unavailable
- Improved unique number generation with collision prevention using set-based tracking
- Fixed type safety issue with null checks on timestamp variables

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack**: Streamlit-based web application
- **Rationale**: Streamlit provides rapid development for data-driven applications with minimal frontend code, ideal for healthcare administrative tools
- **Key Features**: 
  - Real-time UI updates through session state management
  - Geolocation integration via `streamlit_geolocation` component
  - Wide layout configuration for dashboard-style interface
- **Trade-offs**: Limited customization compared to full frontend frameworks, but significantly faster development time for MVP

### State Management

**Approach**: Streamlit session state for persistent data across interactions
- **Core State Variables**:
  - `stage`: Tracks application flow (form submission, queue management)
  - `fila_global`: Global queue list managing all patient check-ins
  - `numero_chamado`: Unique patient queue number
  - `tempo_entrada_posicao_3`: Timestamp tracking for queue position monitoring
  - `passou_posicao_3`: Boolean flag for queue progression logic
  - `ultimo_avanco_fila`: Timestamp for queue advancement throttling
  - `numeros_usados`: Set preventing duplicate queue numbers
- **Rationale**: Session state provides simple persistence without database complexity for prototype/demo purposes
- **Limitation**: Data is session-specific and not shared across users or persisted between restarts

### Geolocation & Proximity Verification

**Implementation**: Client-side geolocation with server-side distance calculation
- **Library**: `geopy` with geodesic distance calculation
- **Validation Logic**: Calculates distance between patient location and health unit coordinates
- **Data Structure**: Dictionary of 10 São Paulo health units with real GPS coordinates
- **Purpose**: Prevents remote check-ins and ensures patients are physically present at facilities
- **Alternative Considered**: GPS spoofing prevention mechanisms (not implemented in current version)

### Queue Management System

**Design Pattern**: Centralized queue with unique identifier generation
- **Number Generation**: Random 4-digit numbers (1000-9999) with collision prevention
- **Queue Tracking**: Array-based position management in `fila_global`
- **Time-based Logic**: Timestamps track when patients reach specific queue positions
- **Advancement Mechanism**: Throttled queue progression using `ultimo_avanco_fila`
- **Rationale**: Simple FIFO queue suitable for single-location scenarios
- **Scalability Consideration**: Current implementation doesn't support multi-facility concurrent queues

### Application Flow Control

**Stage-based Navigation**: Multi-step process managed through `stage` variable
- **Initial Stage**: Form collection (patient information, unit selection)
- **Subsequent Stages**: Queue position display, real-time updates
- **State Transitions**: Controlled through session state modifications
- **Design Choice**: Linear flow prevents users from skipping validation steps

## External Dependencies

### Python Libraries

1. **streamlit** (Core Framework)
   - Purpose: Web application framework and UI rendering
   - Usage: Page configuration, layout management, component rendering

2. **streamlit_geolocation**
   - Purpose: Browser-based geolocation access
   - Usage: Captures patient's current GPS coordinates
   - Integration: Custom Streamlit component for location services

3. **geopy**
   - Purpose: Geographical calculations
   - Specific Module: `geopy.distance.geodesic`
   - Usage: Calculate real-world distances between coordinates in kilometers

4. **datetime** (Standard Library)
   - Purpose: Time tracking and temporal logic
   - Usage: Queue timing, timestamps, duration calculations

5. **random** (Standard Library)
   - Purpose: Queue number generation
   - Usage: Generate unique 4-digit patient identifiers

6. **time** (Standard Library)
   - Purpose: Time-based operations and delays
   - Usage: Potential throttling and timing operations

### Data Sources

**Health Unit Coordinates**: Hard-coded dictionary of 10 São Paulo health facilities
- UBS (Unidade Básica de Saúde) locations
- AMA (Assistência Médica Ambulatorial) locations  
- UPA (Unidade de Pronto Atendimento) locations
- Coordinates sourced for real São Paulo neighborhoods (Vila Mariana, Pinheiros, Santana, etc.)

### Future Integration Considerations

The current architecture supports future integration with:
- Database systems for persistent queue storage
- Real-time notification services
- Multi-facility queue management systems
- Healthcare record systems
- Authentication services for patient identification