<?php
include './analytics/process.php';
?>

<!doctype html>
<html lang="en-US">
  <head>
    <title>DiamondGotCat</title>
    <meta name="description" content="DiamondGotCat - Student・Personal Developer・AI/ML Researcher">
    <link rel="stylesheet" href="https://cdn.diamondgotcat.net/tailwind.css">
  </head>
  <body>
    <main>
      <div class="flex">
        <div class="flex h-screen flex-col justify-between border-e border-gray-100 bg-white" >
          <div class="px-4 py-6">
            <div class="flex space-x-4">
              <img class="rounded-full" src="https://avatars.githubusercontent.com/u/124330624?v=4" alt="" width="25" height="25">
              <span>DiamondGotCat</span>
            </div>
            <ul class="mt-6 space-y-1">
              <li>
                <p class="block rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700" >Home</p>
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
                      <a href="https://x.com/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Twitter (formerly X) </a>
                    </li>
                    <li>
                      <a href="https://github.com/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >GitHub </a>
                    </li>
                    <li>
                      <a href="https://huggingface.co/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >HuggingFace </a>
                    </li>
                    <li>
                      <a href="https://zenn.dev/techcat56/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Zenn </a>
                    </li>
                    <li>
                      <a href="https://qiita.com/DiamondGotCat/" class="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700" >Qiita </a>
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
                <a href="#" class="block transition-colors hover:text-gray-900">DiamondGotCat</a>
              </li>
              <li class="rtl:rotate-180">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 20 20" fill="currentColor" >
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </li>
            </ol>
          </nav>
          <h1 class="text-3xl font-bold">Home</h1>
          <div class="py-4"></div>
          <h2 class="text-xl pb-4">Recent Activity</h2>
          <section id="recent">
            <article class="rounded-xl border-2 border-gray-100 bg-white max-w-150">
              <div class="flex flex-row p-2">
                <div>
                  <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                    <a href="#" class="block shrink-0">
                      <img alt="" src="https://avatars.githubusercontent.com/u/124330624?s=96&v=4" class="size-14 rounded-full object-cover" />
                    </a>
                    <div>
                      <h3 class="font-medium sm:text-lg">
                        Released Zeta 4
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
                  <span class="text-[10px] font-medium sm:text-xs">Zeta LLM - New Release</span>
                </strong>
              </div>
            </article>
          </section>
          <div class="py-4"></div>
          <h2 class="text-xl pb-4">Subdomains<span class="pl-4 text-sm text-gray-500">Only a portion of it is displayed</span></h2>
          <section id="tasks" class="flex flex-row">

            <article class="flex-1 rounded-xl border-2 border-gray-100 bg-white">
              <div class="flex items-start gap-4 p-4 sm:p-6 lg:p-8">
                <a href="#" class="block shrink-0">
                  <img alt="" src="https://avatars.githubusercontent.com/u/211832909?s=200&v=4" class="size-14 rounded-lg object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Zeta LLM
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">Zeta Project Official Website</p>
                  <div class="mt-2 sm:flex sm:items-center sm:gap-2">
                    <p class="hidden sm:block sm:text-xs sm:text-gray-500">zeta.diamondgotcat.net</p>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://zeta.diamondgotcat.net/">
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
                  <img alt="" src="https://icons.diamondgotcat.net/v12-5/Qiita.png" class="size-14 rounded-lg object-cover" />
                </a>
                <div>
                  <h3 class="font-medium sm:text-lg">
                    Analytics
                  </h3>
                  <p class="line-clamp-2 text-sm text-gray-700">Analytics of This Website</p>
                  <div class="mt-2 sm:flex sm:items-center sm:gap-2">
                    <p class="hidden sm:block sm:text-xs sm:text-gray-500">analytics.diamondgotcat.net</p>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <a href="https://analytics.diamondgotcat.net/">
                  <strong class="-me-[2px] -mb-[2px] inline-flex items-center gap-1 rounded-ss-xl rounded-ee-xl bg-blue-600 px-3 py-1.5 text-white" >
                    <span class="text-[10px] font-medium sm:text-xs">></span>
                  </strong>
                </a>
              </div>
            </article>

          </section>
        </div>
      </div>
    </main>
  </body>
</html>