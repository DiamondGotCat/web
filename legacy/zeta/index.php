<?php
include '../analytics/process.php';
?>

<!doctype html>
<html lang="en-US">
  <head>
    <title>Dashboard - Zeta LLM</title>
    <meta name="description" content="Dashboard Page - Zeta LLM Website">
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
                <p class="block rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700" >Dashboard </p>
              </li>
              <li>
                <details class="group [&_summary::-webkit-details-marker]:hidden" >
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
                      <a href="downloads/safetensor" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Safetensor </a>
                    </li>
                    <li>
                      <a href="downloads/gguf" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >GGUF </a>
                    </li>
                    <li>
                      <a href="https://ollama.com/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Ollama </a>
                    </li>
                  </ul>
                </details>
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
                <a href="#" class="block transition-colors hover:text-gray-900">Zeta LLM </a>
              </li>
              <li class="rtl:rotate-180">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </li>
            </ol>
          </nav>
          <h1 class="text-3xl font-bold">Dashboard</h1>
          <div class="py-4"></div>
          <h2 class="text-xl pb-4">Current Status</h2>
          <section id="status">
            <article class="rounded-xl border-2 border-gray-100 bg-white max-w-150">
              <div class="flex flex-row p-2">
                <div>
                  <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                    <a href="#" class="block shrink-0">
                      <img alt="" src="https://avatars.githubusercontent.com/u/124330624?s=96&v=4" class="size-14 rounded-full object-cover" />
                    </a>
                    <div>
                      <h3 class="font-medium sm:text-lg">
                        Zeta 4
                      </h3>
                      <p class="line-clamp-2 text-sm text-gray-700">4th Model from Zeta Project </p>
                      <div class="mt-2 sm:flex sm:items-center sm:gap-2">
                        <p class="hidden sm:block sm:text-xs sm:text-gray-500">DiamondGotCat</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="">
                <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-b-xl bg-blue-600 px-3 py-1.5 text-white w-full" >
                  <span class="text-[10px] font-medium sm:text-xs">Released</span>
                </strong>
              </div>
            </article>
          </section>
          <div class="py-4"></div>
          <h2 class="text-xl pb-4">Tasks</h2>
          <section id="tasks" class="flex flex-row">
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://avatars.githubusercontent.com/u/124330624?s=96&v=4" class="size-14 rounded-full object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Training
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">Zeta 4 </p>
                  <div class="mt-2 sm:flex sm:items-center sm:gap-2">
                    <p class="hidden sm:block sm:text-xs sm:text-gray-500">Manual - DiamondGotCat</p>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-green-600 px-3 py-1.5 text-white" >
                  <span class="text-[10px] font-medium sm:text-xs">Finished</span>
                </strong>
              </div>
            </article>
            <div class="px-2"></div>
            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://avatars.githubusercontent.com/u/124330624?s=96&v=4" class="size-14 rounded-full object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Publish
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">Zeta 4 </p>
                  <div class="mt-2 sm:flex sm:items-center sm:gap-2">
                    <p class="hidden sm:block sm:text-xs sm:text-gray-500">Manual - DiamondGotCat</p>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-green-600 px-3 py-1.5 text-white" >
                  <span class="text-[10px] font-medium sm:text-xs">Finished</span>
                </strong>
              </div>
            </article>
          </section>
          <div class="py-4"></div>
          <h2 class="text-xl pb-4">Downloads</h2>
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
                            <p class="block transition-colors hover:text-gray-900">Zeta LLM </p>
                          </li>
                          <li class="rtl:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                          </li>
                          <li>
                            <a href="downloads/" class="block transition-colors hover:text-gray-900">Downloads </a>
                          </li>
                          <li class="rtl:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                          </li>
                          <li>
                            <a href="downloads/safetensor" class="block transition-colors hover:text-gray-900">Safetensor </a>
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
                            <p class="block transition-colors hover:text-gray-900">Zeta LLM </p>
                          </li>
                          <li class="rtl:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                          </li>
                          <li>
                            <a href="downloads/" class="block transition-colors hover:text-gray-900">Downloads </a>
                          </li>
                          <li class="rtl:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                          </li>
                          <li>
                            <a href="downloads/gguf" class="block transition-colors hover:text-gray-900">GGUF </a>
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