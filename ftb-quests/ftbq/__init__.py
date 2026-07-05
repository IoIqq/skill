"""ftbq - shared core for the FTB Quests Claude skill.

Six modules used by the scripts and tests:

    json5     string-aware JSON5 lexer/parser carrying line/col spans
    ids       deterministic md5 ID + canonical content hash
    canonical hand-rolled JSON5 emitter with sorted keys, byte-stable output
    snbt      1.20.1 SNBT emitter + parser
    audit     DLC-vs-installed audit index / diff / description item-pattern harvest
    deploy    safe deploy: overwrite detection + additive merge + .ftbq-backup
"""

__version__ = "0.3.0"
