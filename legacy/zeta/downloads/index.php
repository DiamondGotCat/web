<?php
include '../../analytics/process.php';
?>

<!doctype html>
<html lang="en-US">
  <head>
    <title>Downloads - Zeta LLM</title>
    <meta name="description" content="Downloads - Zeta LLM Website">
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
                <a href="../" class="Disable: block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Dashboard </a>
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
                      <a href="safetensor" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Safetensor </a>
                    </li>
                    <li>
                      <a href="gguf" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >GGUF </a>
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
                <a href="../" class="block transition-colors hover:text-gray-900">Zeta LLM </a>
              </li>
              <li class="rtl:rotate-180">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </li>
            </ol>
          </nav>
          <h1 class="text-3xl font-bold">Downloads</h1>

          <div class="py-4"></div>

          <section id="downloads">
            <div class="overflow-x-auto rounded-lg border border-gray-100">
              <table class="min-w-full divide-y-2 divide-gray-100">
                <thead class="ltr:text-left rtl:text-right">
                  <tr class="*:font-medium *:text-gray-900">
                    <th class="px-3 py-2 whitespace-nowrap">Name</th>
                    <th class="px-3 py-2 whitespace-nowrap">Link</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr class="*:text-gray-900 *:first:font-medium">
                    <td class="px-3 py-2 whitespace-nowrap">Safetensor</td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <nav aria-label="Breadcrumb">
                        <ol class="flex items-center gap-1 text-sm text-gray-700">
                          <li>
                            <a href="safetensor" class="block transition-colors hover:text-gray-900">Safetensor </a>
                          </li>
                        </ol>
                      </nav>
                    </td>
                  </tr>
                  <tr class="*:text-gray-900 *:first:font-medium">
                    <td class="px-3 py-2 whitespace-nowrap">GGUF</td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <nav aria-label="Breadcrumb">
                        <ol class="flex items-center gap-1 text-sm text-gray-700">
                          <li>
                            <a href="gguf" class="block transition-colors hover:text-gray-900">GGUF </a>
                          </li>
                        </ol>
                      </nav>
                    </td>
                  </tr>
                  <tr class="*:text-gray-900 *:first:font-medium">
                    <td class="px-3 py-2 whitespace-nowrap">Ollama</td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <nav aria-label="Breadcrumb">
                        <ol class="flex items-center gap-1 text-sm text-gray-700">
                          <li>
                            <a href="https://ollama.com/" class="block transition-colors hover:text-gray-900">ollama.com </a>
                          </li>
                          <li class="rtl:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                          </li>
                          <li>
                            <a href="https://ollama.com/DiamondGotCat/" class="block transition-colors hover:text-gray-900">DiamondGotCat </a>
                          </li>
                        </ol>
                      </nav>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </main>
  </body>
</html>