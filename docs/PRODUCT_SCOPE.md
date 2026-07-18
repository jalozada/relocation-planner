# Relocation Planner — Product Scope

## Purpose

Build a local-first relocation planning application that helps individuals
and families organize domestic or international moves.

ARGENTINA_TRANSITION_2026 is the first real project and validation case.

## Current Project

- Origin: Tampa, Florida, United States
- Destination: Mar del Plata, Argentina
- Travelers:
  - Javier
  - Ursula
  - Antonella
- Target departure: Late August or early September 2026
- Current travel plan:
  - TPA to EZE
  - Ground transportation from EZE to Mar del Plata
- Current baggage scenario:
  - 3 bicycle boxes
  - 6 regular checked bags
- Furniture is not being transported.

## MVP Features

1. Relocation projects
2. Travelers
3. Bags
4. Inventory
5. Bag assignments and weight calculations
6. Flights and ground transportation
7. Tasks and checklists
8. Expenses and budget
9. Dashboard

## Core Requirements

- Adding or removing bags must immediately update totals.
- Family names, countries, airlines, fees, and currencies must be data,
  not hard-coded application logic.
- Support more than one relocation project.
- Support multiple currencies.
- Support configurable baggage types and weight limits.
- Support bring, carry-on, buy, sell, donate, optional, and undecided decisions.
- Preserve an understandable and simple user interface.
- Provide CSV or Excel export later.
- Remain useful without internet access.

## Deferred Features

- User accounts
- Cloud hosting
- Mobile application
- Document scan storage
- AI assistant
- Notifications
- Collaboration
- Airline website scraping
- Drag-and-drop packing
- Country-specific immigration automation

## Product Principle

Build one validated feature at a time.

The software must first solve the actual Argentina move before being expanded
into a general commercial or public product.

## Transition Workstreams

The application is a complete relocation transition manager, not only a
packing or baggage planner.

### Core Workstreams

- Project dashboard
- Household members
- Tasks, deadlines, dependencies, and waiting states
- Documents and document requirements
- Assets to bring, sell, donate, discard, give away, or store
- Inventory, bags, shipments, and weight calculations
- Flights and ground transportation
- School transition
- Medical-care transition
- Home and account closeout
- Relocation expenses and expected sale proceeds
- Arrival purchases and first-month setup

### Document Tracking

Document records should support:

- Household member
- Document type
- Purpose or requesting organization
- Requested date
- Agency or provider
- Expected date
- Received date
- Apostille requirement and status
- Translation requirement and status
- Original document location
- Secure digital-backup location
- Carry-on packing status
- Notes

Sensitive document scans will not initially be stored in the application.

### Asset Disposition

Assets not being transported must still be tracked through departure.

Supported decisions:

- Bring
- Sell
- Donate
- Discard
- Give to family
- Store
- Undecided

Asset records should support estimated value, listing price, minimum price,
marketplace, listing status, buyer, pickup deadline, actual proceeds, and a
fallback disposition plan.

Furniture is not being moved for ARGENTINA_TRANSITION_2026, but furniture
should be tracked as sell, donate, discard, or give-away inventory.

### Product Priority

The first usable version should provide:

1. Relocation project
2. Household members
3. Workstreams
4. Tasks with owners, deadlines, dependencies, and statuses
5. Dashboard showing overdue, blocked, waiting, and completed work

Specialized document, asset-disposition, baggage, travel, school, medical,
budget, and arrival modules will be added incrementally after that foundation
is validated.
