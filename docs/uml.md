# Architecture UML

Open with any Mermaid-preview extension (e.g. *Markdown Preview Mermaid Support*).
Two views: (1) layer dependencies, (2) the class diagram.

> If your extension bundles an old Mermaid and the `namespace { }` blocks fail to
> render, just delete the `namespace ... {` / matching `}` lines — the classes and
> relationships render fine without them.

## 1. Layer dependencies (arrows = "depends on")

```mermaid
flowchart TD
    scenes -->|Scene contract| shell
    scenes --> ui_kit

    subgraph chess["games/chess (bounded context)"]
        direction TB
        c_ui["ui<br/>(pygame)"] --> c_app["app<br/>(orchestration)"]
        c_app --> c_domain["domain<br/>(pure rules)"]
    end

    c_ui --> ui_kit
    c_ui -->|implements Scene| shell

    c_domain:::pure

    classDef pure fill:#e7f7e7,stroke:#2e7d32,color:#1b3d1b;
```

`domain` is **pure**: it imports nothing outward (no pygame, no app, no ui). That
green box is the invariant to protect — enforce it with pyright/mypy strict.

## 2. Class diagram

```mermaid
classDiagram
    direction LR

    namespace shell {
        class App {
            +run()
        }
        class SceneManager {
            +Scene current_scene
            +change_scene(scene)
            +run_frame()
        }
        class Scene {
            <<interface>>
            +handle_event(event)
            +update(dt)
            +render(surface)
        }
    }

    namespace scenes {
        class MainMenu
        class VariantSelect
    }

    namespace chess_ui {
        class ChessScene {
            +Color human_color
            +handle_event(event)
            +update(dt)
            +render(surface)
        }
        class Renderer {
            +draw(surface, snapshot)
        }
    }

    namespace chess_app {
        class Session {
            +Position position
            +list~Move~ legal_moves
            +GameResult result
            +step()
            +undo()
        }
        class Player {
            <<interface>>
            +request_move(position, legal_moves) Move
        }
        class HumanPlayer {
            +submit(move)
        }
        class AIPlayer
        class search {
            <<module>>
            +find_best_move(position, variant) Move
        }
        class evaluation {
            <<module>>
            +score_board(position) float
        }
    }

    namespace chess_domain {
        class Variant {
            <<interface>>
            +str name
            +initial_position() Position
            +result(position, legal_moves) GameResult
            +adjust_moves(position, moves) list~Move~
        }
        class ClassicalChess
        class Chess960
        class KingOfTheHill
        class movegen {
            <<module>>
            +legal_moves(position, variant) list~Move~
            +apply(position, move) Position
            +is_square_attacked(position, sq, by) bool
        }
        class pieces {
            <<module>>
            +SLIDERS
            +LEAPERS
        }
        class Position {
            +Board board
            +Color side_to_move
            +CastleRights castle_rights
            +Square en_passant_target
            +piece_at(square)
        }
        class Move {
            <<frozen>>
            +Square frm
            +Square to
            +bool is_en_passant
            +bool is_castle
            +PieceType promotion
        }
        class CastleRights {
            <<frozen>>
        }
        class Color {
            <<enumeration>>
            WHITE
            BLACK
        }
        class PieceType {
            <<enumeration>>
            PAWN KNIGHT BISHOP
            ROOK QUEEN KING
        }
        class GameResult {
            <<enumeration>>
            ONGOING WHITE_WINS
            BLACK_WINS DRAW
        }
    }

    %% shell
    App *-- SceneManager
    SceneManager o-- Scene : current

    %% scene realizations
    Scene <|.. MainMenu
    Scene <|.. VariantSelect
    Scene <|.. ChessScene

    %% scenes wiring
    MainMenu ..> SceneManager
    VariantSelect ..> ChessScene : creates
    VariantSelect ..> Variant : chooses

    %% chess ui
    ChessScene *-- Session
    ChessScene *-- Renderer
    ChessScene *-- HumanPlayer
    ChessScene *-- AIPlayer

    %% chess app
    Player <|.. HumanPlayer
    Player <|.. AIPlayer
    Session o-- Player : white/black
    Session *-- Position : current
    Session ..> Variant
    Session ..> movegen
    AIPlayer ..> search
    search ..> evaluation
    search ..> movegen

    %% domain
    Variant <|.. ClassicalChess
    Variant <|.. Chess960
    Variant <|.. KingOfTheHill
    Chess960 ..> ClassicalChess : delegates
    KingOfTheHill ..> ClassicalChess : delegates
    movegen ..> Position
    movegen ..> Move
    movegen ..> pieces
    Position *-- CastleRights
    Position ..> Color
    Move ..> PieceType
    Variant ..> Position
    Variant ..> GameResult
```

### Legend

| Arrow | Meaning |
| --- | --- |
| `<\|..` | implements / realizes interface |
| `*--` | composition (owns; lifecycle-bound) |
| `o--` | aggregation (references / holds) |
| `..>` | dependency (uses) |
