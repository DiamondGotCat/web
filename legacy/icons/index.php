<?php
include '../analytics/process.php';
?>

<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>DiamondGotIcons</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script defer="" src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script defer src="https://cloud.umami.is/script.js" data-website-id="7ae09061-ec1a-4012-a2b4-2531604a520d"></script>

    <meta name="description" content="DiamondGotIcons - DiamondGotCat's Icons/Brands">
    <meta property="og:title" content="DiamondGotIcons" />
    <meta property="og:description" content="DiamondGotCat's Icons/Brands" />
    <meta property="og:url" content="https://diamondgotcat.net/icons/" />
    <meta property="og:image" content="https://diamondgotcat.net/icons/DiamondGotCat-12-Full_1024.png" />
    <meta name="twitter:card" content="https://diamondgotcat.net/icons/DiamondGotCat-12-Full_1024.png" />

    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="manifest" href="/site.webmanifest">
  </head>
  <body class="bg-black">
    <header>
      <nav class="relative shadow" x-data="{ isOpen: false }">
        <div class="container px-6 py-4 mx-auto">
          <div class="lg:flex lg:items-center lg:justify-between">
            <div class="flex items-center justify-between">
              <a href="/">
                <img alt="" height="20" src="https://diamondgotcat.net/DiamondGotCat-12-Full-No-BG_128.png"/>
              </a>
              <div class="flex lg:hidden">
                <button @click="isOpen = !isOpen" aria-label="toggle menu" class="hover:text-gray-600 focus:outline-none focus:text-gray-600 text-gray-200" type="button" x-cloak="">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" x-show="!isOpen" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 8h16M4 16h16" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" x-show="isOpen" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                </button>
              </div>
            </div>
            <div :class="[isOpen ? 'translate-x-0 opacity-100 ' : 'opacity-0 -translate-x-full']" class="inset-x-0 z-20 w-full px-6 py-4 transition-all duration-300 ease-in-out lg:mt-0 lg:p-0 lg:top-0 lg:relative lg:bg-transparent lg:w-auto lg:opacity-100 lg:translate-x-0 lg:flex lg:items-center bg-black" x-cloak="">
              <div class="flex flex-col -mx-6 lg:flex-row lg:items-center lg:mx-8">
                <a class="px-3 py-2 mx-3 mt-2 transition-colors duration-300 transform rounded-md lg:mt-0 hover:bg-gray-100 text-gray-200" href="https://github.com/DiamondGotCat">GitHub</a>
                <a class="px-3 py-2 mx-3 mt-2 transition-colors duration-300 transform rounded-md lg:mt-0 hover:bg-gray-100 text-gray-200" href="/w">Wiki</a>
                <a class="px-3 py-2 mx-3 mt-2 transition-colors duration-300 transform rounded-md lg:mt-0 hover:bg-gray-100 text-gray-200" href="/res">Resources</a>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </header>
    <main>
      <div class="lg:flex bg-black">
        <div class="flex items-center justify-center w-full px-6 py-8 lg:h-[32rem] lg:w-1/2">
          <div class="max-w-xl">
            <h2 class="font-semibold text-4xl text-white">DiamondGot<span class="text-blue-400">Icons</span></h2>
            <p class="mt-4 lg:text-base text-gray-400">DiamondGotCat's Icons</p>
          </div>
        </div>
        <div class="w-full h-64 lg:w-1/2 lg:h-auto">
          <div class="w-full h-full lg:block hidden bg-cover" style="background-image: url(https://diamondgotcat.net/icons/DiamondGotCat-12-Full_SVG.svg)">
            <div class="w-full h-full opacity-25 bg-black">

            </div>
          </div>
        </div>
      </div>
      <section class="container px-4 mx-auto p-20 text-white" id="guidline">
        <h2 class="font-medium text-white">Guidline</h2>
        <div class="pt-4">
          <div class="font-normal border md:rounded-lg p-2 border-gray-700 bg-gray-800">
            <p class="p-2">Please use images only to represent my respective projects.</p>
            <p class="p-2">Don't use a background that obscures the icon.</p>
          </div>
        </div>
      </section>
      <section class="container px-4 mx-auto p-20" id="downloads">
        <h2 class="font-medium text-white">Downloads</h2>
        <div class="flex flex-col mt-6">
          <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
              <div class="overflow-hidden border md:rounded-lg border-gray-700">
                <table class="min-w-full divide-y divide-gray-700">
                  <thead class="bg-gray-800">
                    <tr>
                      <th class="py-3.5 px-4 font-normal rtl:text-right text-gray-400" scope="col">
                        <button class="flex items-center gap-x-3 focus:outline-none">
                          <span>Name</span>
                          <svg class="h-3" fill="none" viewbox="0 0 10 11" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2.13347 0.0999756H2.98516L5.01902 4.79058H3.86226L3.45549 3.79907H1.63772L1.24366 4.79058H0.0996094L2.13347 0.0999756ZM2.54025 1.46012L1.96822 2.92196H3.11227L2.54025 1.46012Z" fill="currentColor" stroke="currentColor" stroke-width="0.1"></path>
                            <path d="M0.722656 9.60832L3.09974 6.78633H0.811638V5.87109H4.35819V6.78633L2.01925 9.60832H4.43446V10.5617H0.722656V9.60832Z" fill="currentColor" stroke="currentColor" stroke-width="0.1"></path>
                            <path d="M8.45558 7.25664V7.40664H8.60558H9.66065C9.72481 7.40664 9.74667 7.42274 9.75141 7.42691C9.75148 7.42808 9.75146 7.42993 9.75116 7.43262C9.75001 7.44265 9.74458 7.46304 9.72525 7.49314C9.72522 7.4932 9.72518 7.49326 9.72514 7.49332L7.86959 10.3529L7.86924 10.3534C7.83227 10.4109 7.79863 10.418 7.78568 10.418C7.77272 10.418 7.73908 10.4109 7.70211 10.3534L7.70177 10.3529L5.84621 7.49332C5.84617 7.49325 5.84612 7.49318 5.84608 7.49311C5.82677 7.46302 5.82135 7.44264 5.8202 7.43262C5.81989 7.42993 5.81987 7.42808 5.81994 7.42691C5.82469 7.42274 5.84655 7.40664 5.91071 7.40664H6.96578H7.11578V7.25664V0.633865C7.11578 0.42434 7.29014 0.249976 7.49967 0.249976H8.07169C8.28121 0.249976 8.45558 0.42434 8.45558 0.633865V7.25664Z" fill="currentColor" stroke="currentColor" stroke-width="0.3"></path>
                          </svg>
                        </button>
                      </th>
                      <th class="px-12 py-3.5 font-normal rtl:text-right text-gray-400" scope="col">Size </th>
                      <th class="px-4 py-3.5 font-normal rtl:text-right text-gray-400" scope="col">Description </th>
                      <th class="px-4 py-3.5 font-normal rtl:text-right text-gray-400" scope="col">Downloads </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-700 bg-gray-900">
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">Bulk Download</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">All </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">Download All as Bulk Archive File</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-12.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat 12 Symbol</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">1024x1024, 512x512, 256x256 </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of DiamondGotCat Logo (No Text)</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-12-Logo.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat 12 Symbol (No BG)</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">-- </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of DiamondGotCat Logo (No Text, No Background)</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-12-Logo-No-BG.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat 12 Logo</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">1024x2048, 512x1024, 256x512 </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of DiamondGotCat Logo (With Text)</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-12-Full.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat 12 Logo (No BG)</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">-- </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of DiamondGotCat Logo (With Text, No Background)</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-12-Full-No-BG.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat Secure File Format</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">-- </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of DGC-SFF Logo</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-SFF.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="px-4 py-4 font-medium whitespace-nowrap text-sm">
                        <div>
                        <h2 class="font-medium hover:underline text-white">DiamondGotCat Zeta Project</h2>
                        <p class="font-normal text-gray-400">MIT License</p>
                        </div>
                      </td>
                      <td class="px-12 py-4 font-medium whitespace-nowrap text-sm text-white">-- </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <h4 class="text-gray-200">All Size of Zeta Project Logo</h4>
                        </div>
                      </td>
                      <td class="px-4 py-4 whitespace-nowrap text-sm">
                        <div>
                        <a download="" href="DiamondGotCat-Zeta.zip">
                          <div class="inline px-3 py-1 font-normal rounded-full gap-x-2 text-sm text-white bg-gray-800">ZIP 
                          </div>
                        </a>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
    <footer class="bg-black">
      <div class="container flex flex-col items-center justify-between p-6 mx-auto space-y-4 sm:space-y-0 sm:flex-row">
        <a href="#">
          <img alt="" height="20" src="https://diamondgotcat.net/DiamondGotCat-12-Full-No-BG_128.png"/>
        </a>
        <p class="text-gray-300">© 2025 DiamondGotCat</p>
          <div class="flex -mx-2">
            <a aria-label="Github" class="mx-2 transition-colors duration-300 hover:text-blue-500 text-gray-300" href="https://github.com/DiamondGotCat">
              <svg class="w-5 h-5 fill-current" fill="none" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.026 2C7.13295 1.99937 2.96183 5.54799 2.17842 10.3779C1.395 15.2079 4.23061 19.893 8.87302 21.439C9.37302 21.529 9.55202 21.222 9.55202 20.958C9.55202 20.721 9.54402 20.093 9.54102 19.258C6.76602 19.858 6.18002 17.92 6.18002 17.92C5.99733 17.317 5.60459 16.7993 5.07302 16.461C4.17302 15.842 5.14202 15.856 5.14202 15.856C5.78269 15.9438 6.34657 16.3235 6.66902 16.884C6.94195 17.3803 7.40177 17.747 7.94632 17.9026C8.49087 18.0583 9.07503 17.99 9.56902 17.713C9.61544 17.207 9.84055 16.7341 10.204 16.379C7.99002 16.128 5.66202 15.272 5.66202 11.449C5.64973 10.4602 6.01691 9.5043 6.68802 8.778C6.38437 7.91731 6.42013 6.97325 6.78802 6.138C6.78802 6.138 7.62502 5.869 9.53002 7.159C11.1639 6.71101 12.8882 6.71101 14.522 7.159C16.428 5.868 17.264 6.138 17.264 6.138C17.6336 6.97286 17.6694 7.91757 17.364 8.778C18.0376 9.50423 18.4045 10.4626 18.388 11.453C18.388 15.286 16.058 16.128 13.836 16.375C14.3153 16.8651 14.5612 17.5373 14.511 18.221C14.511 19.555 14.499 20.631 14.499 20.958C14.499 21.225 14.677 21.535 15.186 21.437C19.8265 19.8884 22.6591 15.203 21.874 10.3743C21.089 5.54565 16.9181 1.99888 12.026 2Z"></path>
              </svg>
            </a>
          </div>
        </div>
    </footer>
  </body>
</html>
