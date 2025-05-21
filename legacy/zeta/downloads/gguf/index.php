<?php
include '../../../analytics/process.php';
?>

<!doctype html>
<html lang="en-US">
  <head>
    <title>GGUF Downloads - Zeta LLM</title>
    <meta name="description" content="GGUF Downloads - Zeta LLM Website">
    <link rel="stylesheet" href="https://cdn.diamondgotcat.net/tailwind.css">
  </head>
  <body>
    <main>
      <div class="flex">
        <div class="flex h-screen flex-col justify-between border-e border-gray-100 bg-white" >
          <div class="px-4 py-6">
            <div class="flex space-x-4">
              <img class="rounded-lg" src="https://avatars.githubusercontent.com/u/211832909?s=200&v=4" alt="" width="25" height="25">
              <span>Zeta LLM</span>
            </div>
            <ul class="mt-6 space-y-1">
              <li>
                <a href="../../" class="Disable: block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Dashboard </a>
              </li>
              <li>
                  <summary class="flex cursor-pointer items-center justify-between rounded-lg px-4 py-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700" >
                    <span class="text-sm font-medium">Downloads </span>
                    <span class="shrink-0 transition duration-300 group-open:-rotate-180" >
                      <svg xmlns="http://www.w3.org/2000/svg" class="size-5" viewBox="0 0 20 20" fill="currentColor" >
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                      </svg>
                    </span>
                  </summary>
                  <ul class="mt-2 space-y-1 px-4">
                    <li>
                      <a href="../safetensor" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Safetensor </a>
                    </li>
                    <li>
                      <a href="../gguf" class="block rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700" >GGUF </a>
                    </li>
                    <li>
                      <a href="https://ollama.com/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Ollama </a>
                    </li>
                  </ul>
              </li>
              <li>
                <details class="group [&_summary::-webkit-details-marker]:hidden" >
                  <summary class="flex cursor-pointer items-center justify-between rounded-lg px-4 py-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700" >
                    <span class="text-sm font-medium">Links </span>
                    <span class="shrink-0 transition duration-300 group-open:-rotate-180" >
                      <svg xmlns="http://www.w3.org/2000/svg" class="size-5" viewBox="0 0 20 20" fill="currentColor" >
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                      </svg>
                    </span>
                  </summary>
                  <ul class="mt-2 space-y-1 px-4">
                    <li>
                      <a href="https://x.com/Zeta_LLM/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Twitter (formerly X) </a>
                    </li>
                    <li>
                      <a href="https://github.com/Zeta-LLM/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >GitHub </a>
                    </li>
                    <li>
                      <a href="https://huggingface.co/Zeta-LLM/" class="w-full rounded-lg px-4 py-2 [text-align:_inherit] text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >HuggingFace </a>
                    </li>
                  </ul>
                </details>
              </li>
            </ul>
          </div>
          <div class="sticky inset-x-0 bottom-0 border-t border-gray-100">
            <a href="#" class="flex items-center gap-2 bg-white p-4 hover:bg-gray-50" >
              <img alt="" src="https://icons.diamondgotcat.net/v12-5/Yellow.png" class="size-10 rounded-full object-cover" />
              <div>
                <p class="text-xs">
                  <strong class="block font-medium" >Guest</strong >
                  <span>Only Public Content Showing </span>
                </p>
              </div>
            </a>
          </div>
        </div>
        <div class="flex-1 p-8">
          <nav aria-label="Breadcrumb">
            <ol class="flex items-center gap-1 text-sm text-gray-700">
              <li>
                <a href="../../" class="block transition-colors hover:text-gray-900">Zeta LLM </a>
              </li>
              <li class="rtl:rotate-180">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </li>
              <li>
                <a href="../" class="block transition-colors hover:text-gray-900">Downloads </a>
              </li>
              <li class="rtl:rotate-180">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </li>
            </ol>
          </nav>
          <h1 class="text-3xl font-bold">GGUF</h1>

          <div class="py-4"></div>

          <h2 class="text-xl pb-4">static</h2>
          <section id="downloads1" class="flex flex-row">
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 4
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-4-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
            <div class="px-2"></div>
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 3
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-3-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
          </section>
          <div class="py-2"></div>
          <section id="downloads2" class="flex flex-row">
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 2
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-2-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
            <div class="px-2"></div>
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 1
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-1-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
          </section>

          <div class="py-4"></div>

          <h2 class="text-xl pb-4">mradermacher imatrix type 1</h2>
          <section id="downloads1" class="flex flex-row">
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 4
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-4-i1-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
            <div class="px-2"></div>
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 3
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-3-i1-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
          </section>
          <div class="py-2"></div>
          <section id="downloads2" class="flex flex-row">
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 2
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://huggingface.co/mradermacher/Zeta-2-i1-GGUF/">
                    <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                        <span class="text-[10px] font-medium sm:text-xs">></span>
                    </strong>
                </a>
              </div>
            </article>
            <div class="px-2"></div>
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://huggingface.co/avatars/6b97d30ff0bdb5d5c633ba850af739cd.svg" class="size-14 object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta 1
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">mradermacher</p>
                </div>
              </div>
              <div class="flex justify-end">
                <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-red-600 px-3 py-1.5 text-white" >
                    <span class="text-[10px] font-medium sm:text-xs">!</span>
                </strong>
              </div>
            </article>
          </section>
        </div>
      </div>
    </main>
  </body>
  <script src="https://unpkg.com/@barba/core"></script>
  <script>
    barba.init({
      transitions: [{
        name: 'fade',
        leave(data) {
          return new Promise(resolve => {
            data.current.container.classList.add('fade-leave');
            setTimeout(resolve, 500);
          });
        },
        enter(data) {
          data.next.container.classList.add('fade-enter');
          setTimeout(() => {
            data.next.container.classList.add('fade-enter-active');
          }, 10);
        }
      }]
    });
  </script>
</html>