# Comic lettering cleanup

The first generations added incidental slogans to books, signs and mugs, despite requests for only a few dialogue lines. Those slogans conflicted with the publication's voice. The first files are preserved as `neg*/assets/comic-first.png`; the corrected editions use `comic.png`.

Each first-generation image was inspected and passed as a local reference to ImageGen with this edit instruction:

> Edit this exact comic image. Preserve every figure, composition, panel, color, scratchy woodcut line and the main visual action. Remove ALL incidental writing from EVERY mug, book spine, poster, wall sign, tool, box and loose paper, replacing it with plain textured surfaces or non-linguistic decorative hatching. The ONLY lettering allowed anywhere in the final image is: [whitelist]. Delete every other word, slogan, aphorism or caption; do not add any new lettering. This is editorial cleanup, not a redesign.

Whitelists:

- -100: “WILL I LOOK DIFFERENT?” and “ONLY UNDERNEATH.”
- -060: “ONE LITTLE PATCH.”, “ARE YOU NAMING IT NOW?” and the title “One Little Patch” on the decorated card.
- -019: “CHECK”, “ELABORATE” and “WE CAN STILL DISAGREE.”

The edited outputs retain the scene and primary dialogue. Some tiny pseudo-engraving remains on the -060 ruler; at publication size it reads as surface texture. No motivational slogans remain on its prominent signs, mugs or books. Future image QA should inspect props as well as speech balloons. Generated lettering belongs to the publication's editorial voice even if nobody requested it.
