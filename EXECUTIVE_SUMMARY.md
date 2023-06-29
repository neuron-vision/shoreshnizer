# TL;DR
Rootnyzer is designed to optimize information preservation while maintaining efficiency for downstream applications, specifically generative Language Models (LLMs) running on edge devices with limited resources.

By prioritizing the preservation of the root of words, Rootnyzer achieves a compact representation that retains the essential semantic content. This approach allows for a reduction in the overall dimensionality of the language model input, enabling it to run smoothly on resource-constrained devices.

The compact representation produced by Rootnyzer serves as an input to the generative LLM. Since the root carries a significant portion of the word's meaning, focusing on it ensures that the generated language output remains coherent and contextually relevant. This approach also allows for a more efficient training process for the LLM, as the reduced input dimensionality requires less computational resources and data for training.

The ability to run generative LLMs on edge devices opens up possibilities for various applications, including real-time language processing, on-device language translation, text generation, and more. By leveraging the optimized information preservation and compact representation offered by Rootnyzer, these applications can operate efficiently and effectively on devices with limited computational power and storage capacity.

# תקציר

על ידי התמקדות בשמירה על השורש של המילים, Rootnyzer משיג ייצוג קומפקטי משמר תוכן סמנטי. באמצעות שיטה זו, ניתן להפחית את ממדיות הקלט הכוללות של דגם השפה, ולכן הרצת הדגם תהיה חלקה ויעילה יותר על התקנים המוגבלים במשאבים.

המיומנות של Rootnyzer לשמירה היעילה על המידע משמשת כקלט ל-LLM. מאחר והשורש מכיל חלק ניכר מהמשמעות של המילה, התמקדות בו מבטיחה שפלט השפה הנוצרת ישמר קשר קונטקסטואלי ומתאים. שיטה זו מאפשרת גם תהליך אימון יעיל יותר של ה-LLM, כיוון שהממדיות המופחתות של הקלט דורשות פחות משאבים חישוביים ומידע עבור אימון.

היכולת להריץ LLMs מחולקים על התקנים קצה מאפשרת אפשרויות מגוונות שליישומים, כולל חילול שפה בזמן אמת.


# A picture


![Overview Diagram](https://www.freecodecamp.org/news/content/images/size/w2000/2021/10/IMG_0079.jpg)

The diagram is linked from [The Evolution of Tokenization – Byte Pair Encoding in NLP](https://www.freecodecamp.org/news/evolution-of-tokenization/)
