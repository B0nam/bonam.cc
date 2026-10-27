---
title: "FIWARE: the heart of smart cities"
date: 2026-04-13T12:01:02+00:00
slug: "fiware-the-heart-of-smart-cities"
description: "What FIWARE is and how its Context Broker, NGSI entities and IoT agents give smart cities a common data language for traffic, lighting and more."
locale: "en_US"
categories:
    - "Smart Cities"
image: "01-1-wmcb-z3c5vqbue8rurtl4g.png"
tags:
    - "future"
    - "iot"
    - "technology"
    - "fiware"
    - "smart-cities"
    - "english"
canonicalUrl: "https://danibonam.medium.com/fiware-the-heart-of-smart-cities-66d9905f454e"
mediumUrl: "https://danibonam.medium.com/fiware-the-heart-of-smart-cities-66d9905f454e"
sitemap:
    disable: true
---
## What is FIWARE

FIWARE is an open-source platform that provides standardized components to accelerate the development of applications in the context of smart resources and services.

Born in 2011 as an initiative of the European Commission in partnership with major technology companies, the FIWARE ecosystem is now present in cities, farms, industries, ports, energy networks, and many other domains that depend on real-time data.

In a smart city, FIWARE acts as a “brain” that integrates data from traffic, parking, public lighting, environment, and safety into a unified, real-time context view. Instead of each system living in its own silo, everything starts speaking the same language, enabling faster decisions and smarter public services.

![](02-0-klubimuoqnxhrczc.png)

### How FIWARE sees the city

For the FIWARE platform, a city (or any other smart environment) is broken down into abstractions. Each part of the real world becomes a digital context element that can be queried and updated in real time.

- **Entities**: represent elements of the city, such as parking spots, streetlights, buses, bins, sensors, and so on. Each of these physical elements has a “digital copy” inside the platform, called an entity.
- **Attributes**: describe the state of these entities. A parking spot may have attributes such as occupied/free; a streetlight may have attributes such as light intensity and energy consumption. In short, attributes are the pieces of information that characterize each entity at a given moment.
- **Verticals**: are the major business domains in which entities are organized, such as mobility, public lighting, safety, environment, energy, sanitation, and others. Each vertical has its own types of entities, but they all share the same context language.
- **Context**: is the digital representation of the current state of these entities. Put simply, it is the “snapshot of the moment” of the city, seen through its digital objects.

In this way, FIWARE can abstract real-world elements of the city into a standardized context model. This allows different solutions and vendors to see the same urban reality without depending on a single proprietary system.

![](03-0-kmaflcgk5vre0afm.jpg)

## The FIWARE architecture

From an architectural point of view, FIWARE is not a single system; it is a set of components that, combined, form a smart platform. Each solution uses only the building blocks needed for its use case, always built around a central element called the *Context Broker*.

![](04-0-wqfe2rcw7cusyub2.png)

### Context Broker: the core of the platform

The Context Broker is the component responsible for maintaining and exposing the context in real time, that is, the up-to-date state of the entities that represent the city. It exposes the context API for creating, updating, querying, and subscribing to changes, acting as the central integration point for all other blocks.

### Generic Enablers: building blocks around context

Around the Context Broker, FIWARE offers several components called *Generic Enablers*. They extend the capabilities of the platform by enabling the integration of devices and sensors through IoT connectors, processing and storing data for history, analysis, and insights, as well as handling identity, authentication, and authorization to protect the city’s APIs and resources.

### Applications and systems consuming context

On top of this base, web and mobile applications, operational dashboards, open data platforms, and even legacy city systems can consume the context exposed by FIWARE. From there, each team or vendor can build smart services on top of the same city view, without having to reinvent the integration layer.

## Conclusion

FIWARE was born as a concrete response to the chaos of isolated systems that exists in many cities: instead of each solution living in its own world, the platform proposes a common context language and a well-defined core, the Context Broker, around which everything connects.

By representing the city through standardized entities and attributes and providing pluggable blocks for IoT, data, and security, FIWARE creates a solid foundation for different teams, vendors, and startups to build smart services on top of the same urban reality.

In other words, FIWARE works as a common language for countless systems, allowing them to finally work together in building the connected future of smart cities.
