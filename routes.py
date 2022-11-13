from core.router import Router, Route, CallBack

router = Router("File Store Router",
                Route("Main Menu", "Main menu description ...",
                      children=(
                          Route("create user", callback=CallBack("public.utils", "create_user")),
                          Route("see files", callback=CallBack("public.utils", "see_files")),
                          Route("Login", callback=CallBack("public.utils", "Login")),
                          Route("add file", callback=CallBack("public.utils", "add_file")),
                          Route("buy file", callback=CallBack("public.utils", "buy_file")),
                          Route("add comment", callback=CallBack("public.utils", "add_comment")),
                          )),
                      )

